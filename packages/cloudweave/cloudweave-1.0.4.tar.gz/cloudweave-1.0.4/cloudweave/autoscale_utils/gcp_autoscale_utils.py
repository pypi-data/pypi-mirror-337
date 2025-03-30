import time
import asyncio
import async_timeout
from typing import Dict, Any, Optional, Tuple, List, Set

from cloudweave.logging_manager import Logger
from cloudweave.cloud_session_utils.gcp_session_manager import GCPManager
from cloudweave.autoscale_utils.exceptions import InstanceGroupError, ComputeError
from cloudweave.autoscale_utils.state_manager import StateManager
from cloudweave.autoscale_utils.data_utils import NetworkConfig
from cloudweave.autoscale_utils.async_utils import AsyncRetry


class InstanceGroupManager:
    """Manages GCP Instance Group operations."""
    
    def __init__(self, instance_group_name, zone, **kwargs):
        self.instance_group_name = instance_group_name
        self.zone = zone
        self.project_id = kwargs.get('project_id')
        self.retry = AsyncRetry(
            retries=kwargs.get('gcp_retry_attempts', 3),
            initial_delay=kwargs.get('retry_delay', 2.0),
            logger_options=kwargs.get('logger_options', {})
        )
        self.gcp_manager = GCPManager.instance(kwargs)
        
        # Setup logger
        self._setup_logger(kwargs.get('logger_options', {}))
        
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """Set up the logger for this Instance Group Manager."""
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info(f"Using provided logger instance for InstanceGroupManager with group {self.instance_group_name}")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', 'instance-group-manager')
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f'ig-{self.instance_group_name}'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for InstanceGroupManager with namespace '{log_namespace}'")
    
    @property
    def compute_client(self):
        return self.gcp_manager.get_client('compute')
    
    @AsyncRetry(retries=3)
    async def get_instance_group_info(self):
        """Get information about the Instance Group."""
        start_time = time.time()
        try:
            instance_group = await asyncio.to_thread(
                self.compute_client.instance_groups().get,
                project=self.project_id,
                zone=self.zone,
                instanceGroup=self.instance_group_name
            ).execute
            
            if not instance_group:
                raise InstanceGroupError(f"Instance Group {self.instance_group_name} not found or empty response")
                
            duration = time.time() - start_time
            
            return instance_group
            
        except Exception as e:            
            if isinstance(e, InstanceGroupError):
                raise
                
            raise InstanceGroupError(f"Error getting Instance Group info: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def get_instance_group_size(self):
        """Get current size of the Instance Group."""
        try:
            instance_group = await self.get_instance_group_info()
            return instance_group.get('size', 0)
        except Exception as e:
            self.logger.error(f"Error getting Instance Group size: {str(e)}")
            raise InstanceGroupError(f"Error getting Instance Group size: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def get_instance_group_target_size(self):
        """Get target size of the Instance Group."""
        try:
            instance_group_manager = await asyncio.to_thread(
                self.compute_client.instanceGroupManagers().get,
                project=self.project_id,
                zone=self.zone,
                instanceGroupManager=self.instance_group_name
            ).execute
            
            return instance_group_manager.get('targetSize', 0)
        except Exception as e:
            self.logger.error(f"Error getting Instance Group target size: {str(e)}")
            raise InstanceGroupError(f"Error getting Instance Group target size: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def get_instances(self):
        """Get instances in the Instance Group."""
        try:
            response = await asyncio.to_thread(
                self.compute_client.instanceGroups().listInstances,
                project=self.project_id,
                zone=self.zone,
                instanceGroup=self.instance_group_name,
                body={"instanceState": "ALL"}
            ).execute
            
            instances = []
            
            for instance in response.get('items', []):
                instance_id = instance.get('instance').split('/')[-1]
                status = instance.get('status')
                instances.append((
                    instance_id,
                    status,
                    instance.get('status')  # Using status as health for now
                ))
                
            return instances
        except Exception as e:
            self.logger.error(f"Error getting Instance Group instances: {str(e)}")
            raise InstanceGroupError(f"Error getting Instance Group instances: {str(e)}") from e
    
    async def resize_instance_group(self, new_size):
        """Resize the Instance Group."""
        start_time = time.time()
        
        try:
            current_size = await self.get_instance_group_size()
            target_size = await self.get_instance_group_target_size()
            
            if new_size <= current_size:
                self.logger.info(f"No need to resize: current size {current_size} >= requested size {new_size}")
                return False
            
            resize_request = await asyncio.to_thread(
                self.compute_client.instanceGroupManagers().resize,
                project=self.project_id,
                zone=self.zone,
                instanceGroupManager=self.instance_group_name,
                size=new_size
            ).execute
            
            operation_name = resize_request.get('name')
            if not operation_name:
                raise InstanceGroupError("Resize operation failed, no operation name returned")
            
            # Wait for the resize operation to complete
            await self._wait_for_operation(operation_name)
            
            self.logger.info(f"Resized Instance Group from {current_size} to {new_size}")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            raise InstanceGroupError(f"Error resizing Instance Group: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def delete_instance(self, instance_id):
        """Delete a Compute Engine instance."""
        try:
            delete_request = await asyncio.to_thread(
                self.compute_client.instances().delete,
                project=self.project_id,
                zone=self.zone,
                instance=instance_id
            ).execute
            
            operation_name = delete_request.get('name')
            if not operation_name:
                raise InstanceGroupError("Delete operation failed, no operation name returned")
            
            # Wait for the delete operation to complete
            await self._wait_for_operation(operation_name)
            
            self.logger.info(f"Deleted instance {instance_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete instance {instance_id}: {str(e)}")
            raise InstanceGroupError(f"Error deleting instance: {str(e)}") from e
    
    async def _wait_for_operation(self, operation_name, timeout=300):
        """Wait for a zonal operation to complete."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                operation = await asyncio.to_thread(
                    self.compute_client.zoneOperations().get,
                    project=self.project_id,
                    zone=self.zone,
                    operation=operation_name
                ).execute
                
                if operation.get('status') == 'DONE':
                    if 'error' in operation:
                        raise InstanceGroupError(f"Operation failed: {operation['error']}")
                    return True
                
                await asyncio.sleep(2)
            except Exception as e:
                if isinstance(e, InstanceGroupError):
                    raise
                
                raise InstanceGroupError(f"Error checking operation status: {str(e)}") from e
        
        raise TimeoutError(f"Operation {operation_name} timed out")


class ContainerManager:
    """Manages Docker container operations on GCE instances."""
    
    def __init__(self, instance_group_manager, network_config, container_image, **kwargs):
        self.instance_group_manager = instance_group_manager
        self.network_config = network_config
        self.container_image = container_image
        self.project_id = kwargs.get('project_id')
        self.zone = kwargs.get('zone')
        self.retry = AsyncRetry(
            retries=kwargs.get('gcp_retry_attempts', 3),
            initial_delay=kwargs.get('retry_delay', 2.0),
            logger_options=kwargs.get('logger_options', {})
        )
        
        self.gcp_manager = GCPManager.instance(kwargs)
        
        # Setup logger
        self._setup_logger(kwargs.get('logger_options', {}))
        
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """Set up the logger for this Container Manager instance."""
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info(f"Using provided logger instance for ContainerManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', 'container-manager')
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', 'container-manager'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for ContainerManager with namespace '{log_namespace}'")
    
    @property
    def compute_client(self):
        return self.gcp_manager.get_client('compute')
    
    async def verify_container_status(self, instance_id):
        """Verify container status on an instance using SSH."""
        start_time = time.time()
        consecutive_failures = 0
        container_verification_timeout = 300  # Default timeout if not in kwargs
        max_consecutive_failures = 5    # Default if not in kwargs
        retry_delay = 2.0               # Default if not in kwargs
        
        while time.time() - start_time < container_verification_timeout:
            try:
                # TODO, you would use SSH or GCP APIs to check container status
                # For this example, we'll simulate success after a short delay
                await asyncio.sleep(5)
                
                self.logger.info(f"Container verified for instance {instance_id}")
                return True
                
            except Exception as e:
                consecutive_failures += 1
                self.logger.warning(f"Error verifying container for {instance_id}: {str(e)}")
                
                if consecutive_failures >= max_consecutive_failures:
                    raise ComputeError(f"Failed to verify container after {consecutive_failures} attempts")
                    
                await asyncio.sleep(retry_delay)
        
        raise TimeoutError(f"Container verification timeout for instance {instance_id}")
    
    @AsyncRetry(retries=3)
    async def get_instance_info(self, instance_id):
        """Get detailed information about a GCE instance."""
        try:
            instance = await asyncio.to_thread(
                self.compute_client.instances().get,
                project=self.project_id,
                zone=self.zone,
                instance=instance_id
            ).execute
            
            return instance
            
        except Exception as e:
            self.logger.error(f"Error getting instance info for {instance_id}: {str(e)}")
            raise ComputeError(f"Error getting instance info: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def start_container(self, instance_id):
        """Start a container on a GCE instance."""
        try:
            # TODO, you would use SSH or GCP APIs to start the container
            # For this example, we'll simulate success after a short delay
            await asyncio.sleep(2)
            
            self.logger.info(f"Started container on instance {instance_id}")
            return {
                'instance_id': instance_id,
                'container_id': f"container-{instance_id}",
                'status': 'running'
            }
        except Exception as e:
            self.logger.error(f"Error starting container on {instance_id}: {str(e)}")
            raise ComputeError(f"Error starting container: {str(e)}") from e


class GCPAutoscaleManager:
    """Manages GCP autoscaling operations with improved error handling and monitoring."""
    
    def __init__(self, **kwargs):
        """Initialize autoscale manager."""
        # Store all options in self.opt
        self.opt = kwargs.copy()
        
        # Validate required fields
        required_fields = [
            "container_image", "region", "zone", "instance_group_name", 
            "project_id", "network", "subnetwork", "name_space"
        ]
        self._validate_inputs(self.opt, required_fields)
        
        # Initialize instance attributes from self.opt
        self.container_image = self.opt["container_image"]
        self.region = self.opt["region"]
        self.zone = self.opt["zone"]
        self.instance_group_name = self.opt['instance_group_name']
        self.project_id = self.opt['project_id']
        self.retry_count = 0
        
        # Setup logger
        self._setup_logger(self.opt.get('logger_options', {}))
        
        # Create network configuration
        self.network_config = NetworkConfig(
            network=self.opt['network'],
            subnetwork=self.opt['subnetwork']
        )
        
        # Set up managers for different responsibilities
        self._initialize_managers()
        
        # State tracking
        self.problematic_instances = set()
        self.state_manager = StateManager()
        
        self.gcp_manager = GCPManager.instance(self.opt)
        self.logger.info("GCPAutoscaleManager initialized successfully", extra={'opt': self.opt})
        
    def _validate_inputs(self, inputs, required_fields):
        """Validate that required fields are present in the inputs."""
        missing_fields = [field for field in required_fields if field not in inputs]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """Set up the logger for this Autoscale Manager instance."""
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for GCPAutoscaleManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', self.opt.get('name_space', 'gcp-autoscale-manager'))
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', 'gcp-autoscale-manager'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for GCPAutoscaleManager with namespace '{log_namespace}'")
    
    def _initialize_managers(self):
        """Initialize component managers with shared configuration."""
        # Prepare logger options for child managers
        logger_options = {'logger_instance': self.logger}
        
        # Create Instance Group and Container managers with shared logger
        self.instance_group_manager = InstanceGroupManager(
            self.instance_group_name,
            self.zone,
            project_id=self.project_id,
            logger_options=logger_options, 
            **self.opt
        )
        
        self.container_manager = ContainerManager(
            self.instance_group_manager,
            self.network_config,
            self.container_image,
            project_id=self.project_id,
            zone=self.zone,
            logger_options=logger_options,
            **self.opt
        )
        
    async def get_available_instance(self):
        """Get an available instance for container execution."""
        try:
            # Get initial instances
            initial_instances_list = await self.instance_group_manager.get_instances()
            initial_instances = {instance[0] for instance in initial_instances_list}
            
            # Check if we already have instances
            if not initial_instances:
                self.logger.info("No instances found in Instance Group, checking configuration")
                
                # Resize Instance Group
                current_size = await self.instance_group_manager.get_instance_group_size()
                if not await self.instance_group_manager.resize_instance_group(current_size + 1):
                    self.logger.warning("Failed to resize Instance Group.")
                    return None
            else:
                self.logger.info(f"Found {len(initial_instances)} existing instances in Instance Group")
                
                # If we reach here, we need a new instance
                self.logger.info("No existing usable instances found, resizing Instance Group")
                
                current_size = await self.instance_group_manager.get_instance_group_size()
                if not await self.instance_group_manager.resize_instance_group(current_size + 1):
                    self.logger.warning("Failed to resize Instance Group.")
                    return None
            
            # Wait for new instance with retries
            start_time = time.time()
            check_count = 0
            max_wait_time = self.opt.get('max_wait_time', 600)
            
            while time.time() - start_time < max_wait_time:
                check_count += 1
                
                # Get current instances
                current_instances_list = await self.instance_group_manager.get_instances()
                current_instances = {instance[0] for instance in current_instances_list}
                
                # Find new instances
                new_instances = current_instances - initial_instances
                
                # Check if we've found any new instances
                for instance_id in new_instances:
                    try:
                        # Verify the instance is ready for container operations
                        if await self.container_manager.verify_container_status(instance_id):
                            self.logger.info(f"Found new available instance: {instance_id} after {check_count} checks")
                            return instance_id
                    except Exception as e:
                        self.logger.error(f"Error checking new instance {instance_id}: {str(e)}")
                
                # Wait before next check
                await asyncio.sleep(5)
                
            self.logger.error(f"Timeout waiting for new instance after {max_wait_time}s")
            return None
                
        except Exception as e:
            if isinstance(e, InstanceGroupError):
                raise
                
            raise InstanceGroupError(f"Error getting available instance: {str(e)}") from e
    
    async def _cleanup_on_failure(self):
        """Clean up resources after a failure."""
        self.logger.info("Cleaning up resources after failure")
        
        # Implement TODO cleanup logic here
        # For example, delete problematic instances
        
        return True
    
    async def _cleanup_resources(self):
        """Clean up resources at the end of execution."""
        self.logger.info("Cleaning up resources")
        
        # Implement TODO cleanup logic here
        
        return True
            
    async def run(self):
        """Execute autoscaling operation with timeout and state management."""
        try:
            max_wait_time = self.opt.get('max_wait_time', 600)
            async with async_timeout.timeout(max_wait_time):
                try:
                    return await self.autoscale()
                except Exception as e:
                    self.state_manager.transition_to("CLEANUP")
                    await self._cleanup_on_failure()
                    raise RuntimeError(f"Autoscaling failed: {str(e)}") from e
                        
        except asyncio.TimeoutError:
            self.state_manager.transition_to("ERROR")
            self.logger.error("Autoscaling operation timed out")
            await self._cleanup_on_failure()
            raise RuntimeError("Autoscaling operation timed out")
            
        except Exception as e:
            self.state_manager.transition_to("ERROR")
            self.logger.error(f"Critical error in autoscaling: {str(e)}")
            raise
            
        finally:
            await self._cleanup_resources()
            
    async def autoscale(self):
        """Execute main autoscaling logic with proper state transitions."""
        instance_id = None
        container_id = None
        start_time = time.time()
        max_retries = self.opt.get('max_retries', 3)
        
        try:
            # Step 1: Enter scaling state
            self.state_manager.transition_to("SCALING")
            
            # Step 2: Get available instance
            instance_id = await self.get_available_instance()
            
            if not instance_id:
                self.logger.warning(
                    f"Failed to get available instance (attempt {self.retry_count + 1} "
                    f"of {max_retries + 1})"
                )
                
                return {'instance_id': None, 'container_id': None}
                
            # Step 3: Enter instance setup state
            self.state_manager.transition_to("INSTANCE_SETUP")
            
            # Step 4: Get instance info
            instance_info = await self.container_manager.get_instance_info(instance_id)
            if not instance_info:
                raise RuntimeError(f"Failed to get instance info for {instance_id}")
            
            # Step 5: Enter container starting state
            self.state_manager.transition_to("CONTAINER_STARTING")
            
            try:
                # Step 6: Start container
                response = await self.container_manager.start_container(instance_id)
                
                # Extract container ID from the response
                if response and 'container_id' in response:
                    container_id = response.get('container_id')
                    self.logger.info(f"Started container: {container_id} on instance {instance_id}")
                
                # Step 7: Enter completed state
                self.state_manager.transition_to("COMPLETED")
                self.logger.info("Autoscaling completed successfully")
                
            except Exception as container_error:
                # Handle container start failure
                self.state_manager.transition_to("ERROR")
                
                if instance_id:
                    await self.instance_group_manager.delete_instance(instance_id)
                    self.problematic_instances.add(instance_id)
                    
                raise container_error
                
        except Exception as e:
            # Handle overall failure
            self.state_manager.transition_to("ERROR")
            self.logger.error(f"Autoscaling failed: {str(e)}")
            
            if instance_id and instance_id not in self.problematic_instances:
                try:
                    await self.instance_group_manager.delete_instance(instance_id)
                    self.problematic_instances.add(instance_id)
                except Exception as cleanup_error:
                    self.logger.error(f"Failed to delete instance {instance_id}: {str(cleanup_error)}")
                    
            raise
                
        # Return both instance ID and container ID for monitoring
        return {
            'instance_id': instance_id,
            'container_id': container_id
        }


if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Logger options
        logger_options = {
            "logger_type": "local",
            "namespace": "gcp-autoscale-example",
            "instance_id": "main-runner",
            "log_level": "info"
        }
        
        logger = Logger(**logger_options)
        logger.info("Starting GCP autoscale example")
        
        # Configuration for GCPAutoscaleManager
        config = {
            "container_image": "gcr.io/my-project/my-container:latest",
            "region": "us-central1",
            "zone": "us-central1-a",
            "instance_group_name": "my-instance-group",
            "project_id": "my-gcp-project",
            "network": "default",
            "subnetwork": "default",
            "name_space": "gcp-autoscale-example",
            "logger_options": {"logger_instance": logger}
        }
        
        try:
            # Initialize GCPAutoscaleManager with our config
            manager = GCPAutoscaleManager(**config)
            
            # Run the autoscaling operation
            logger.info("Starting autoscale operation")
            result = await manager.run()
            
            # Get the instance ID and container ID from the result
            instance_id = result.get('instance_id')
            container_id = result.get('container_id')
            
            if instance_id:
                logger.info(f"Successfully started instance {instance_id} with container {container_id}")
                
                # Wait some time to let the container run (e.g., 5 minutes)
                logger.info(f"Waiting for 5 minutes before deleting instance {instance_id}")
                await asyncio.sleep(300)  # 5 minutes
                
                # Delete the instance
                logger.info(f"Deleting instance {instance_id}")
                await manager.instance_group_manager.delete_instance(instance_id)
                logger.info(f"Instance {instance_id} deleted successfully")
            else:
                logger.error("Failed to start an instance")
        
        except Exception as e:
            logger.error(f"Error in GCP autoscale example: {str(e)}")
            raise
        finally:
            logger.info("GCP autoscale example completed")
    
    # Run the async main function
    asyncio.run(main())