import time
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum

from cloudweave.logging_manager import Logger

class AutoscaleState(str, Enum):
    """State machine states for the autoscaling process."""
    INITIALIZING = "initializing"
    SCALING = "scaling"
    INSTANCE_SETUP = "instance_setup"
    TASK_STARTING = "task_starting"
    CLEANUP = "cleanup"
    ERROR = "error"
    COMPLETED = "completed"

class StateManager:
    """Manages state transitions and validation."""
    
    def __init__(self, 
               namespace: str,
               instance_id: Optional[str] = None,
               logger_options: Dict[str, Any] = None,
               initial_state: Optional[AutoscaleState] = None,
               **kwargs):
        self._state = initial_state
        self.namespace = namespace
        self.instance_id = instance_id
        
        self._setup_logger(logger_options or {})
        
        self._state_history = [(time.time(), initial_state)]
        self._valid_transitions = {
            AutoscaleState.INITIALIZING: {
                AutoscaleState.SCALING, 
                AutoscaleState.ERROR
            },
            AutoscaleState.SCALING: {
                AutoscaleState.INSTANCE_SETUP, 
                AutoscaleState.CLEANUP,
                AutoscaleState.ERROR
            },
            AutoscaleState.INSTANCE_SETUP: {
                AutoscaleState.TASK_STARTING, 
                AutoscaleState.CLEANUP,
                AutoscaleState.ERROR
            },
            AutoscaleState.TASK_STARTING: {
                AutoscaleState.COMPLETED, 
                AutoscaleState.CLEANUP,
                AutoscaleState.ERROR
            },
            AutoscaleState.CLEANUP: {
                AutoscaleState.COMPLETED,
                AutoscaleState.ERROR
            },
            AutoscaleState.ERROR: {
                AutoscaleState.CLEANUP
            },
            AutoscaleState.COMPLETED: set()
        }
        
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this Autoscale State Manager instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for Autoscale state manager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', f"autoscale-{self.namespace}")
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f"autoscale-state-manager-{self.namespace}"),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for Autoscale State Manager with namespace '{log_namespace}'")
        
    @property
    def state(self) -> AutoscaleState:
        """Get current state."""
        return self._state
        
    @property
    def state_history(self) -> List[Tuple[float, AutoscaleState]]:
        """Get state transition history."""
        return self._state_history.copy()
        
    def can_transition_to(self, new_state: AutoscaleState) -> bool:
        """
        Check if transition to new state is valid.
        
        Args:
            new_state: Target state
            
        Returns:
            True if transition is valid
        """
        return new_state in self._valid_transitions[self._state]
        
    def transition_to(self, new_state: AutoscaleState) -> None:
        """
        Transition to new state if valid.
        
        Args:
            new_state: Target state
            
        Raises:
            ValueError: If transition is invalid
        """
        if not self.can_transition_to(new_state):
            current = self._state
            self.logger.error(f"Invalid state transition: {current} -> {new_state}")
            raise ValueError(f"Invalid state transition: {current} -> {new_state}")
            
        self._state = new_state
        self._state_history.append((time.time(), new_state))
        self.logger.info(f"State transition: {new_state}")
        
    def is_error_state(self) -> bool:
        """Check if current state is error state."""
        return self._state == AutoscaleState.ERROR
        
    def is_final_state(self) -> bool:
        """Check if current state is final state."""
        return self._state in (AutoscaleState.COMPLETED, AutoscaleState.ERROR)