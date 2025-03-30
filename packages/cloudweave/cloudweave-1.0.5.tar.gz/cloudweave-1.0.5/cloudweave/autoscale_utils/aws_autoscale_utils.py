import time
import asyncio
import async_timeout
from typing import Dict, Any, Optional, Tuple, List, Set

from cloudweave.cloud_session_utils.aws_session_manager import AWSManager
from cloudweave.logging_manager import Logger

from cloudweave.autoscale_utils.exceptions import ASGError, ECSError
from cloudweave.autoscale_utils.state_manager import StateManager
from cloudweave.autoscale_utils.data_utils import NetworkConfig
from cloudweave.autoscale_utils.async_utils import AsyncRetry


class ASGManager:
    """Manages Auto Scaling Group operations."""
    
    def __init__(self, asg_name, **kwargs):
        self.asg_name = asg_name
        self.retry = AsyncRetry(
            retries=kwargs.get('aws_retry_attempts', 3),
            initial_delay=kwargs.get('retry_delay', 2.0),
            logger_options=kwargs.get('logger_options', {})
        )
        self.aws_manager = AWSManager.instance(kwargs)
        
        # Setup logger
        self._setup_logger(kwargs.get('logger_options', {}))
        
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """Set up the logger for this ASG Manager instance."""
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info(f"Using provided logger instance for ASGManager with ASG {self.asg_name}")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', 'asg-manager')
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f'asg-{self.asg_name}'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for ASGManager with namespace '{log_namespace}'")
        
    @property
    def asg_client(self):
        return self.aws_manager.asg
    
    @property
    def ec2_client(self):
        return self.aws_manager.ec2
        
    @AsyncRetry(retries=3)
    async def get_asg_info(self):
        """Get information about the Auto Scaling Group."""
        start_time = time.time()
        try:
            response = await asyncio.to_thread(
                self.asg_client.describe_auto_scaling_groups,
                AutoScalingGroupNames=[self.asg_name]
            )
            
            if not response or 'AutoScalingGroups' not in response or not response['AutoScalingGroups']:
                raise ASGError(f"ASG {self.asg_name} not found or empty response")
                
            duration = time.time() - start_time
            
            return response['AutoScalingGroups'][0]
            
        except Exception as e:
            duration = time.time() - start_time
            
            if isinstance(e, ASGError):
                raise
                
            raise ASGError(f"Error getting ASG info: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def get_asg_capacity(self):
        """Get current capacity of the Auto Scaling Group."""
        try:
            asg_info = await self.get_asg_info()
            return asg_info.get('DesiredCapacity', 0)
        except Exception as e:
            self.logger.error(f"Error getting ASG capacity: {str(e)}")
            raise ASGError(f"Error getting ASG capacity: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def get_asg_max_capacity(self):
        """Get maximum capacity of the Auto Scaling Group."""
        try:
            asg_info = await self.get_asg_info()
            return asg_info.get('MaxSize', 0)
        except Exception as e:
            self.logger.error(f"Error getting ASG max capacity: {str(e)}")
            raise ASGError(f"Error getting ASG max capacity: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def get_asg_instances(self):
        """Get instances in the Auto Scaling Group."""
        try:
            asg_info = await self.get_asg_info()
            instances = []
            
            for instance in asg_info.get('Instances', []):
                instances.append((
                    instance.get('InstanceId'),
                    instance.get('LifecycleState'),
                    instance.get('HealthStatus')
                ))
                
            return instances
        except Exception as e:
            self.logger.error(f"Error getting ASG instances: {str(e)}")
            raise ASGError(f"Error getting ASG instances: {str(e)}") from e
    
    async def scale_up_asg(self, increment=None):
        """Scale up the Auto Scaling Group."""
        start_time = time.time()
        # Use default increment if none provided
        increment = increment or 1
        
        try:
            current_capacity = await self.get_asg_capacity()
            max_capacity = await self.get_asg_max_capacity()
            
            if current_capacity >= max_capacity:
                self.logger.info(f"Cannot scale up: at maximum capacity ({max_capacity})")
                return False
                
            new_capacity = min(current_capacity + increment, max_capacity)
            
            await asyncio.to_thread(
                self.asg_client.set_desired_capacity,
                AutoScalingGroupName=self.asg_name,
                DesiredCapacity=new_capacity,
                HonorCooldown=False
            )
            
            self.logger.info(f"Scaled up ASG from {current_capacity} to {new_capacity}")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            raise ASGError(f"Error scaling up ASG: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def terminate_instance(self, instance_id):
        """Terminate an EC2 instance."""
        try:
            await asyncio.to_thread(
                self.ec2_client.terminate_instances,
                InstanceIds=[instance_id]
            )
            
            self.logger.info(f"Terminated instance {instance_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to terminate instance {instance_id}: {str(e)}")
            raise ASGError(f"Error terminating instance: {str(e)}") from e


class ECSManager:
    """Manages ECS cluster and task operations."""
    
    def __init__(self, cluster_name, task_definition_family, network_config, asg_manager, **kwargs):
        self.cluster_name = cluster_name
        self.task_definition_family = task_definition_family
        self.network_config = network_config
        self.asg_manager = asg_manager
        self.retry = AsyncRetry(
            retries=kwargs.get('aws_retry_attempts', 3),
            initial_delay=kwargs.get('retry_delay', 2.0),
            logger_options=kwargs.get('logger_options', {})
        )
        
        self.aws_manager = AWSManager.instance(kwargs)
        
        # Setup logger
        self._setup_logger(kwargs.get('logger_options', {}))
        
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """Set up the logger for this ECS Manager instance."""
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info(f"Using provided logger instance for ECSManager with cluster {self.cluster_name}")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', 'ecs-manager')
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f'ecs-{self.cluster_name}'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for ECSManager with namespace '{log_namespace}'")
        
    @property
    def ecs_client(self):
        return self.aws_manager.ecs
        
    async def verify_ecs_agent_registration(self, instance_id):
        """Verify ECS agent registration for an instance."""
        start_time = time.time()
        consecutive_failures = 0
        ecs_registration_timeout = 300  # Default timeout if not in kwargs
        max_consecutive_failures = 5    # Default if not in kwargs
        retry_delay = 2.0               # Default if not in kwargs
        
        while time.time() - start_time < ecs_registration_timeout:
            try:
                response = await asyncio.to_thread(
                    self.ecs_client.list_container_instances,
                    cluster=self.cluster_name,
                    filter=f"ec2InstanceId == '{instance_id}'"
                )
                
                if response.get('containerInstanceArns'):
                    container_details = await asyncio.to_thread(
                        self.ecs_client.describe_container_instances,
                        cluster=self.cluster_name,
                        containerInstances=[response['containerInstanceArns'][0]]
                    )
                    
                    if container_details.get('containerInstances'):
                        instance = container_details['containerInstances'][0]
                        if instance.get('status') == 'ACTIVE' and instance.get('agentConnected'):
                            self.logger.info(f"ECS agent registered for instance {instance_id}")
                            
                            return True
                
                consecutive_failures = 0
                await asyncio.sleep(retry_delay)
                
            except Exception as e:
                consecutive_failures += 1
                self.logger.warning(f"Error verifying ECS agent for {instance_id}: {str(e)}")
                
                if consecutive_failures >= max_consecutive_failures:
                    raise ECSError(f"Failed to verify ECS agent after {consecutive_failures} attempts")
                    
                await asyncio.sleep(retry_delay)
        
        raise TimeoutError(f"ECS agent registration timeout for instance {instance_id}")
    
    @AsyncRetry(retries=3)
    async def get_container_instance(self, instance_id):
        """Get container instance ARN for an EC2 instance."""
        try:
            response = await asyncio.to_thread(
                self.ecs_client.list_container_instances,
                cluster=self.cluster_name,
                filter=f"ec2InstanceId == '{instance_id}'"
            )
            
            if not response.get('containerInstanceArns'):
                self.logger.warning(f"No container instance found for EC2 instance {instance_id}")
                return None
                
            return response['containerInstanceArns'][0]
        except Exception as e:
            self.logger.error(f"Error getting container instance for {instance_id}: {str(e)}")
            raise ECSError(f"Error getting container instance: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def start_task(self, container_instance_arn):
        """Start an ECS task on a container instance."""
        try:
            latest_task_def = await self._get_latest_task_definition()
            
            response = await asyncio.to_thread(
                self.ecs_client.start_task,
                cluster=self.cluster_name,
                containerInstances=[container_instance_arn],
                taskDefinition=latest_task_def,
                networkConfiguration={
                    'awsvpcConfiguration': {
                        'subnets': self.network_config.subnets,
                        'securityGroups': self.network_config.security_groups,
                        'assignPublicIp': 'ENABLED'
                    }
                }
            )
            
            self.logger.info(f"Started task with definition {latest_task_def}")
            return response
        except Exception as e:
            self.logger.error(f"Error starting task: {str(e)}")
            raise ECSError(f"Error starting task: {str(e)}") from e
    
    @AsyncRetry(retries=3)
    async def _get_latest_task_definition(self):
        """Get the latest task definition ARN."""
        try:
            response = await asyncio.to_thread(
                self.ecs_client.list_task_definitions,
                familyPrefix=self.task_definition_family,
                sort='DESC',
                status='ACTIVE',
                maxResults=1
            )
            
            if not response.get('taskDefinitionArns'):
                raise ECSError(f"No task definitions found for family {self.task_definition_family}")
                
            return response['taskDefinitionArns'][0]
        except Exception as e:
            self.logger.error(f"Error getting latest task definition: {str(e)}")
            raise ECSError(f"Error getting latest task definition: {str(e)}") from e


class AWSAutoscaleManager:
    """Manages AWS autoscaling operations with improved error handling and monitoring."""
    
    def __init__(self, **kwargs):
        """Initialize autoscale manager."""
        # Store all options in self.opt
        self.opt = kwargs.copy()
        
        # Validate required fields
        required_fields = [
            "task_definition_family", "region", "asg_name", 
            "cluster_name", "subnets","security_groups", "name_space"
        ]
        self._validate_inputs(self.opt, required_fields)
        
        # Initialize instance attributes from self.opt
        self.task_definition_family = self.opt["task_definition_family"]
        self.region = self.opt["region"]
        self.asg_name = self.opt['asg_name']
        self.cluster_name = self.opt['cluster_name']
        self.launch_type = self.opt.get('launch_type', 'ON_DEMAND')
        self.retry_count = 0
        
        # Setup logger
        self._setup_logger(self.opt.get('logger_options', {}))
        
        # Create network configuration
        self.network_config = NetworkConfig(
            subnets=self.opt['subnets'],
            security_groups=self.opt['security_groups']
        )
        
        # Set up managers for different responsibilities
        self._initialize_managers()
        
        # State tracking
        self.problematic_instances = set()
        self.state_manager = StateManager()
        
        self.aws_manager = AWSManager.instance(self.opt)
        self.logger.info("AutoscaleManager initialized successfully", extra={'opt': self.opt})
        
    def _validate_inputs(self, inputs, required_fields):
        """Validate that required fields are present in the inputs."""
        missing_fields = [field for field in required_fields if field not in inputs]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """Set up the logger for this Autoscale Manager instance."""
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for AutoscaleManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', self.opt.get('name_space', 'autoscale-manager'))
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', 'autoscale-manager'),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for AutoscaleManager with namespace '{log_namespace}'")
    
    def _initialize_managers(self):
        """Initialize component managers with shared configuration."""
        # Prepare logger options for child managers
        logger_options = {'logger_instance': self.logger}
        
        # Create ASG and ECS managers with shared logger
        self.asg_manager = ASGManager(
            self.asg_name, 
            logger_options=logger_options, 
            **self.opt
        )
        
        self.ecs_manager = ECSManager(
            self.cluster_name,
            self.task_definition_family,
            self.network_config,
            self.asg_manager,
            logger_options=logger_options,
            **self.opt
        )
        
    @property
    def asg_client(self):
        return self.aws_manager.asg
        
    async def get_available_instance(self):
        """Get an available instance for task execution."""
        try:
            # Get initial instances
            initial_instances_list = await self.asg_manager.get_asg_instances()
            initial_instances = {instance[0] for instance in initial_instances_list}
            
            # Check if we already have instances
            if not initial_instances:
                self.logger.info("No instances found in ASG, checking ASG configuration")
                
                # Scale up ASG
                if not await self.asg_manager.scale_up_asg():
                    self.logger.warning("Failed to scale up ASG. Check max capacity and scaling policies.")
                    return None
            else:
                self.logger.info(f"Found {len(initial_instances)} existing instances in ASG")
                
                # If we reach here, we need a new instance
                self.logger.info("No existing usable instances found, scaling up ASG")
                
                if not await self.asg_manager.scale_up_asg():
                    self.logger.warning("Failed to scale up ASG. Forcing creation of a new instance.")
                    
                    # Get current ASG info
                    asg_info = await self.asg_manager.get_asg_info()
                    current_capacity = asg_info.get('DesiredCapacity', 0)
                    
                    # Force an explicit increase in capacity
                    try:
                        await asyncio.to_thread(
                            self.asg_client.set_desired_capacity,
                            AutoScalingGroupName=self.asg_name,
                            DesiredCapacity=current_capacity + 1,
                            HonorCooldown=False
                        )
                        self.logger.info(f"Forced ASG capacity from {current_capacity} to {current_capacity + 1}")
                    except Exception as force_error:
                        self.logger.error(f"Failed to force new instance creation: {str(force_error)}")
                        return None
            
            # Wait for new instance with retries for scaling up
            start_time = time.time()
            check_count = 0
            max_wait_time = self.opt.get('max_wait_time', 600)
            
            while time.time() - start_time < max_wait_time:
                check_count += 1
                
                # Get current instances
                current_instances_list = await self.asg_manager.get_asg_instances()
                current_instances = {instance[0] for instance in current_instances_list}
                
                # Find new instances
                new_instances = current_instances - initial_instances
                
                # Check if we've found any new instances
                for instance_id in new_instances:
                    try:
                        # Verify the instance is properly registered with ECS
                        if await self.ecs_manager.verify_ecs_agent_registration(instance_id):
                            self.logger.info(f"Found new available instance: {instance_id} after {check_count} checks")
                            return instance_id
                    except Exception as e:
                        self.logger.error(f"Error checking new instance {instance_id}: {str(e)}")
                
                # Wait before next check
                await asyncio.sleep(5)
                
            self.logger.error(f"Timeout waiting for new instance after {max_wait_time}s")
            return None
                
        except Exception as e:
            if isinstance(e, ASGError):
                raise
                
            raise ASGError(f"Error getting available instance: {str(e)}") from e
    
    async def _cleanup_on_failure(self):
        """Clean up resources after a failure."""
        self.logger.info("Cleaning up resources after failure")
        
        # Implement TODO cleanup logic here
        # For example, terminate problematic instances
        
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
                    await self.autoscale()
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
        task_arn = None
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
                
                return {'instance_id': None, 'task_arn': None}
                
            # Step 3: Enter instance setup state
            self.state_manager.transition_to("INSTANCE_SETUP")
            
            # Step 4: Get container instance
            container_arn = await self.ecs_manager.get_container_instance(instance_id)
            if not container_arn:
                raise RuntimeError(f"Failed to get container instance ARN for {instance_id}")
            
            # Step 5: Enter task starting state
            self.state_manager.transition_to("TASK_STARTING")
            
            try:
                # Step 6: Start task
                response = await self.ecs_manager.start_task(container_arn)
                
                # Extract task ARN from the response
                if response and 'tasks' in response and len(response['tasks']) > 0:
                    task_arn = response['tasks'][0].get('taskArn')
                    self.logger.info(f"Started task: {task_arn}")
                
                # Step 7: Enter completed state
                self.state_manager.transition_to("COMPLETED")
                self.logger.info("Autoscaling completed successfully")
                
            except Exception as task_error:
                # Handle task start failure
                self.state_manager.transition_to("ERROR")
                
                if instance_id:
                    await self.asg_manager.terminate_instance(instance_id)
                    self.problematic_instances.add(instance_id)
                    
                raise task_error
                
        except Exception as e:
            # Handle overall failure
            self.state_manager.transition_to("ERROR")
            self.logger.error(f"Autoscaling failed: {str(e)}")
            
            if instance_id and instance_id not in self.problematic_instances:
                try:
                    await self.asg_manager.terminate_instance(instance_id)
                    self.problematic_instances.add(instance_id)
                except Exception as cleanup_error:
                    self.logger.error(f"Failed to terminate instance {instance_id}: {str(cleanup_error)}")
                    
            raise
                
        # Return both instance ID and task ARN for monitoring
        return {
            'instance_id': instance_id,
            'task_arn': task_arn
        }
        
        
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Logger options
        logger_options = {
            "logger_type": "local",
            "namespace": "autoscale-example",
            "instance_id": "main-runner",
            "log_level": "info"
        }
        
        logger = Logger(**logger_options)
        logger.info("Starting autoscale example")
        
        # Configuration for AutoscaleManager
        config = {
            "task_definition_family": "my-task-family",
            "region": "us-west-2",
            "asg_name": "my-asg-group",
            "cluster_name": "my-ecs-cluster",
            "subnets": ["subnet-12345", "subnet-67890"],
            "security_groups": ["sg-12345"],
            "name_space": "autoscale-example",
            "logger_options": {"logger_instance": logger}
        }
        
        try:
            # Initialize AutoscaleManager with our config
            manager = AWSAutoscaleManager(**config)
            
            # Run the autoscaling operation
            logger.info("Starting autoscale operation")
            result = await manager.run()
            
            # Get the instance ID from the result
            instance_id = result.get('instance_id')
            task_arn = result.get('task_arn')
            
            if instance_id:
                logger.info(f"Successfully started instance {instance_id} with task {task_arn}")
                
                # Wait some time to let the task run (e.g., 5 minutes)
                logger.info(f"Waiting for 5 minutes before terminating instance {instance_id}")
                await asyncio.sleep(300)  # 5 minutes
                
                # Terminate the instance
                logger.info(f"Terminating instance {instance_id}")
                await manager.asg_manager.terminate_instance(instance_id)
                logger.info(f"Instance {instance_id} terminated successfully")
            else:
                logger.error("Failed to start an instance")
        
        except Exception as e:
            logger.error(f"Error in autoscale example: {str(e)}")
            raise
        finally:
            logger.info("Autoscale example completed")
    
    # Run the async main function
    asyncio.run(main())