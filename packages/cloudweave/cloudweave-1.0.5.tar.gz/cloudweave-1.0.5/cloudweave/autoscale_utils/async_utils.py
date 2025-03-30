import asyncio
from typing import Dict, Any

from cloudweave.logging_manager import Logger

class AsyncRetry:
    """Async retry decorator with backoff."""
    
    def __init__(
        self, 
        retries=3, 
        backoff_base=2.0,
        initial_delay=1.0,
        max_delay=60.0,
        exceptions=(Exception,),
        logger_options: Dict[str, Any] = None,
    ):
        """
        Initialize retry decorator.
        
        Args:
            retries: Maximum retry attempts
            backoff_base: Backoff multiplier
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exceptions: Exceptions to catch and retry
            logger_options: Logger configuration options
        """
        self.retries = retries
        self.backoff_base = backoff_base
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exceptions = exceptions
        self._setup_logger(logger_options or {})
        
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this Async Retry instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for AsyncRetry")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', 'async-retry')
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', 'async-retry-decorator'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for AsyncRetry with namespace '{log_namespace}'")
        
    def __call__(self, func):
        """Apply decorator to function."""
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(self.retries + 1):
                try:
                    return await func(*args, **kwargs)
                    
                except self.exceptions as e:
                    last_exception = e
                    
                    if attempt < self.retries:
                        delay = min(
                            self.initial_delay * (self.backoff_base ** attempt),
                            self.max_delay
                        )
                        
                        self.logger.info(
                            f"Retry {attempt+1}/{self.retries} for {func.__name__} "
                            f"after {delay:.2f}s: {str(e)}"
                        )
                        
                        await asyncio.sleep(delay)
                    else:
                        self.logger.error(
                            f"Failed after {self.retries} retries for {func.__name__}: {str(e)}"
                        )
                        
            # If we get here, we've exhausted all retries
            assert last_exception is not None
            raise last_exception
            
        return wrapper