import enum
import time
import asyncio
import async_timeout
from typing import Dict, Any, Optional, Tuple, List, Set, Union, Type
from threading import Lock

# Import AWS components
from cloudweave.autoscale_utils import ASGManager, ECSManager, AWSAutoscaleManager
from cloudweave.autoscale_utils import InstanceGroupManager, ContainerManager, GCPAutoscaleManager

# Import other utilities
from cloudweave.autoscale_utils.exceptions import AutoscaleError, ASGError, ECSError, InstanceGroupError, ComputeError
from cloudweave.autoscale_utils.state_manager import StateManager
from cloudweave.autoscale_utils.data_utils import NetworkConfig
from cloudweave.autoscale_utils.async_utils import AsyncRetry

# Import logger
from cloudweave.logging_manager import Logger, LoggerType
# Import cloud managers
from cloudweave.cloud_session_utils.aws_session_manager import AWSManager
from cloudweave.cloud_session_utils.gcp_session_manager import GCPManager


class CloudProviderType(enum.Enum):
    """Enum for supported cloud provider types."""
    AWS = "aws"
    GCP = "gcp"
    
    @classmethod
    def from_string(cls, value: str) -> 'CloudProviderType':
        """Convert string to enum value."""
        try:
            return cls(value.lower())
        except ValueError:
            valid_values = ', '.join([e.value for e in cls])
            raise ValueError(f"Invalid cloud provider type: {value}. Valid values are: {valid_values}")


class AutoscaleManager:
    """
    Unified autoscale manager for multiple cloud providers.
    Supports AWS and GCP with a consistent interface.
    """
    
    # Registry of autoscale manager instances
    _registry = {}
    _lock = Lock()
    
    def __init__(self, 
                 cloud_provider: Union[str, CloudProviderType],
                 instance_id: Optional[str] = None,
                 logger_options: Dict[str, Any] = None,
                 **kwargs):
        """
        Initialize an autoscale manager.
        
        Args:
            cloud_provider: Type of cloud provider to use (AWS or GCP)
            instance_id: Optional unique identifier for this autoscale manager
            logger_options: Optional logger configuration
            **kwargs: Cloud provider-specific autoscale parameters
        """
        # Convert string to enum if necessary
        if isinstance(cloud_provider, str):
            self.cloud_provider = CloudProviderType.from_string(cloud_provider)
        else:
            self.cloud_provider = cloud_provider
            
        # Generate unique instance ID if not provided
        self.instance_id = instance_id or f"autoscale-{self.cloud_provider.value}-{time.time()}"
        
        # Store options for later use
        self.opt = kwargs.copy()
        
        # Initialize the logger
        self._setup_logger(logger_options or {})
        
        # Initialize the autoscale manager for the specific cloud provider
        self._initialize_autoscale_manager()
        
        # Register this instance
        with AutoscaleManager._lock:
            AutoscaleManager._registry[self.instance_id] = self
            
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this Autoscale Manager instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for AutoscaleManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', f"autoscale-{self.cloud_provider.value}")
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f"autoscale-{self.cloud_provider.value}-{self.instance_id}"),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for AutoscaleManager with namespace '{log_namespace}'")
    
    def _initialize_autoscale_manager(self):
        """Initialize the specific cloud provider's autoscale manager."""
        try:
            # Initialize autoscale manager based on cloud provider
            if self.cloud_provider == CloudProviderType.AWS:
                self._validate_aws_inputs()
                # Set up logger options to pass to AWS autoscale manager
                logger_options = {'logger_instance': self.logger}
                
                # Create AWS autoscale manager
                self.manager = AWSAutoscaleManager(
                    logger_options=logger_options, 
                    **self.opt
                )
                self.logger.info("AWS AutoscaleManager initialized successfully")
                
            elif self.cloud_provider == CloudProviderType.GCP:
                self._validate_gcp_inputs()
                # Set up logger options to pass to GCP autoscale manager
                logger_options = {'logger_instance': self.logger}
                
                # Create GCP autoscale manager
                self.manager = GCPAutoscaleManager(
                    logger_options=logger_options, 
                    **self.opt
                )
                self.logger.info("GCP AutoscaleManager initialized successfully")
                
            else:
                error_msg = f"Unsupported cloud provider: {self.cloud_provider}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            self.logger.error(f"Failed to initialize autoscale manager: {e}")
            raise
    
    def _validate_aws_inputs(self):
        """Validate that required fields for AWS are present in the inputs."""
        required_fields = [
            "task_definition_family", "region", "asg_name", 
            "cluster_name", "subnets", "security_groups", "name_space"
        ]
        
        missing_fields = [field for field in required_fields if field not in self.opt]
        if missing_fields:
            raise ValueError(f"Missing required fields for AWS: {', '.join(missing_fields)}")
    
    def _validate_gcp_inputs(self):
        """Validate that required fields for GCP are present in the inputs."""
        required_fields = [
            "container_image", "region", "zone", "instance_group_name", 
            "project_id", "network", "subnetwork", "name_space"
        ]
        
        missing_fields = [field for field in required_fields if field not in self.opt]
        if missing_fields:
            raise ValueError(f"Missing required fields for GCP: {', '.join(missing_fields)}")
    
    @classmethod
    def get_instance(cls, instance_id: str) -> Optional['AutoscaleManager']:
        """
        Get an autoscale manager instance by ID.
        
        Args:
            instance_id: Autoscale manager instance ID
            
        Returns:
            AutoscaleManager instance or None if not found
        """
        return cls._registry.get(instance_id)
        
    @classmethod
    def list_instances(cls) -> List[str]:
        """
        List all registered autoscale manager instance IDs.
        
        Returns:
            List of instance IDs
        """
        return list(cls._registry.keys())
    
    async def run(self, **kwargs):
        """
        Execute autoscaling operation with timeout and state management.
        Delegates to the specific cloud provider's manager.
        
        Args:
            **kwargs: Additional parameters to pass to the run method
            
        Returns:
            Result from the autoscaling operation
        """
        self.logger.info("Starting autoscale operation")
        try:
            result = await self.manager.run(**kwargs)
            self.logger.info("Autoscale operation completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Autoscale operation failed: {e}")
            raise
    
    async def get_available_instance(self):
        """
        Get an available instance for execution.
        Delegates to the specific cloud provider's manager.
        
        Returns:
            Instance ID or None if no instance is available
        """
        self.logger.info("Getting available instance")
        try:
            instance_id = await self.manager.get_available_instance()
            if instance_id:
                self.logger.info(f"Found available instance: {instance_id}")
            else:
                self.logger.warning("No available instance found")
            return instance_id
        except Exception as e:
            self.logger.error(f"Error getting available instance: {e}")
            raise
    
    async def terminate_instance(self, instance_id: str):
        """
        Terminate an instance by ID.
        Delegates to the specific cloud provider's manager.
        
        Args:
            instance_id: ID of the instance to terminate
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Terminating instance: {instance_id}")
        try:
            if self.cloud_provider == CloudProviderType.AWS:
                result = await self.manager.asg_manager.terminate_instance(instance_id)
            elif self.cloud_provider == CloudProviderType.GCP:
                result = await self.manager.instance_group_manager.delete_instance(instance_id)
            else:
                raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
                
            if result:
                self.logger.info(f"Instance {instance_id} terminated successfully")
            else:
                self.logger.warning(f"Failed to terminate instance {instance_id}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error terminating instance {instance_id}: {e}")
            raise
    
    async def get_instances(self):
        """
        Get a list of current instances.
        Delegates to the specific cloud provider's manager.
        
        Returns:
            List of instances with their status
        """
        self.logger.info("Getting current instances")
        try:
            if self.cloud_provider == CloudProviderType.AWS:
                instances = await self.manager.asg_manager.get_asg_instances()
            elif self.cloud_provider == CloudProviderType.GCP:
                instances = await self.manager.instance_group_manager.get_instances()
            else:
                raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
                
            self.logger.info(f"Found {len(instances)} instances")
            return instances
        except Exception as e:
            self.logger.error(f"Error getting instances: {e}")
            raise
    
    async def scale_up(self, increment: int = 1):
        """
        Scale up the instance group or ASG by the specified increment.
        Delegates to the specific cloud provider's manager.
        
        Args:
            increment: Number of instances to add
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Scaling up by {increment} instances")
        try:
            if self.cloud_provider == CloudProviderType.AWS:
                result = await self.manager.asg_manager.scale_up_asg(increment)
            elif self.cloud_provider == CloudProviderType.GCP:
                # Get current size
                current_size = await self.manager.instance_group_manager.get_instance_group_size()
                result = await self.manager.instance_group_manager.resize_instance_group(current_size + increment)
            else:
                raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
                
            if result:
                self.logger.info(f"Scaled up successfully")
            else:
                self.logger.warning(f"Failed to scale up")
                
            return result
        except Exception as e:
            self.logger.error(f"Error scaling up: {e}")
            raise
    
    async def wait_for_instance_ready(self, instance_id: str, timeout: int = 300):
        """
        Wait for an instance to become ready.
        Delegates to the specific cloud provider's manager.
        
        Args:
            instance_id: ID of the instance to check
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if instance is ready, False if timed out
        """
        self.logger.info(f"Waiting for instance {instance_id} to become ready")
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    if self.cloud_provider == CloudProviderType.AWS:
                        result = await self.manager.ecs_manager.verify_ecs_agent_registration(instance_id)
                    elif self.cloud_provider == CloudProviderType.GCP:
                        result = await self.manager.container_manager.verify_container_status(instance_id)
                    else:
                        raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
                        
                    if result:
                        self.logger.info(f"Instance {instance_id} is ready")
                        return True
                except Exception as e:
                    self.logger.debug(f"Instance not ready yet, retrying: {e}")
                    
                await asyncio.sleep(5)
                
            self.logger.warning(f"Timed out waiting for instance {instance_id} to become ready")
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for instance readiness: {e}")
            raise
    
    async def start_container(self, instance_id: str):
        """
        Start a container on the given instance.
        Delegates to the specific cloud provider's manager.
        
        Args:
            instance_id: ID of the instance to start container on
            
        Returns:
            Container details if successful
        """
        self.logger.info(f"Starting container on instance {instance_id}")
        try:
            if self.cloud_provider == CloudProviderType.AWS:
                container_instance = await self.manager.ecs_manager.get_container_instance(instance_id)
                if not container_instance:
                    raise AutoscaleError(f"No container instance found for {instance_id}")
                    
                result = await self.manager.ecs_manager.start_task(container_instance)
            elif self.cloud_provider == CloudProviderType.GCP:
                result = await self.manager.container_manager.start_container(instance_id)
            else:
                raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
                
            self.logger.info(f"Container started successfully on instance {instance_id}")
            return result
        except Exception as e:
            self.logger.error(f"Error starting container on instance {instance_id}: {e}")
            raise
    
    def get_native_manager(self):
        """
        Get the native autoscale manager instance.
        
        Returns:
            The underlying autoscale manager (AWSAutoscaleManager or GCPAutoscaleManager)
        """
        return self.manager


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def aws_example():
        # Logger options
        logger_options = {
            "logger_type": "local",
            "namespace": "autoscale-example",
            "instance_id": "aws-runner",
            "log_level": "info"
        }
        
        # Configuration for AWS autoscaling
        aws_config = {
            "task_definition_family": "my-task-family",
            "region": "us-west-2",
            "asg_name": "my-asg-group",
            "cluster_name": "my-ecs-cluster",
            "subnets": ["subnet-12345", "subnet-67890"],
            "security_groups": ["sg-12345"],
            "name_space": "autoscale-example"
        }
        
        # Initialize AWS autoscale manager
        aws_manager = AutoscaleManager(
            cloud_provider="aws",
            instance_id="aws-example",
            logger_options=logger_options,
            **aws_config
        )
        
        # Run autoscaling operation
        print("Starting AWS autoscale operation")
        result = await aws_manager.run()
        print(f"AWS autoscale result: {result}")
        
        # Get the instance ID from the result
        instance_id = result.get('instance_id')
        if instance_id:
            print(f"Successfully started AWS instance {instance_id}")
            
            # Wait 5 minutes
            print(f"Waiting for 5 minutes before terminating instance {instance_id}")
            await asyncio.sleep(300)
            
            # Terminate the instance
            print(f"Terminating instance {instance_id}")
            await aws_manager.terminate_instance(instance_id)
            print(f"Instance {instance_id} terminated successfully")
        else:
            print("Failed to start an AWS instance")
    
    async def gcp_example():
        # Logger options
        logger_options = {
            "logger_type": "local",
            "namespace": "gcp-autoscale-example",
            "instance_id": "gcp-runner",
            "log_level": "info"
        }
        
        # Configuration for GCP autoscaling
        gcp_config = {
            "container_image": "gcr.io/my-project/my-container:latest",
            "region": "us-central1",
            "zone": "us-central1-a",
            "instance_group_name": "my-instance-group",
            "project_id": "my-gcp-project",
            "network": "default",
            "subnetwork": "default",
            "name_space": "gcp-autoscale-example"
        }
        
        # Initialize GCP autoscale manager
        gcp_manager = AutoscaleManager(
            cloud_provider="gcp",
            instance_id="gcp-example",
            logger_options=logger_options,
            **gcp_config
        )
        
        # Run autoscaling operation
        print("Starting GCP autoscale operation")
        result = await gcp_manager.run()
        print(f"GCP autoscale result: {result}")
        
        # Get the instance ID from the result
        instance_id = result.get('instance_id')
        if instance_id:
            print(f"Successfully started GCP instance {instance_id}")
            
            # Wait 5 minutes
            print(f"Waiting for 5 minutes before terminating instance {instance_id}")
            await asyncio.sleep(300)
            
            # Terminate the instance
            print(f"Terminating instance {instance_id}")
            await gcp_manager.terminate_instance(instance_id)
            print(f"Instance {instance_id} terminated successfully")
        else:
            print("Failed to start a GCP instance")
    
    async def main():
        try:
            # List all available autoscale manager instances
            print("Available autoscale managers:", AutoscaleManager.list_instances())
            
            # Run both examples
            await aws_example()
            await gcp_example()
            
            # List all autoscale manager instances after running examples
            print("Available autoscale managers after running:", AutoscaleManager.list_instances())
            
            # Get specific autoscale manager instance
            aws_manager = AutoscaleManager.get_instance("aws-example")
            if aws_manager:
                print(f"Retrieved AWS autoscale manager with ID: {aws_manager.instance_id}")
                instances = await aws_manager.get_instances()
                print(f"Current AWS instances: {instances}")
                
            gcp_manager = AutoscaleManager.get_instance("gcp-example")
            if gcp_manager:
                print(f"Retrieved GCP autoscale manager with ID: {gcp_manager.instance_id}")
                instances = await gcp_manager.get_instances()
                print(f"Current GCP instances: {instances}")
                
        except Exception as e:
            print(f"Error in main: {e}")
    
    # Run the async main function
    asyncio.run(main())