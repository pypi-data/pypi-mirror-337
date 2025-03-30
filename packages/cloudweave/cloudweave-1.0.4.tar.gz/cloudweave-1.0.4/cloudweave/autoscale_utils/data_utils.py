#data_utils.py
from typing import Dict, Any, Optional, Set, List, Union, Tuple, Type, TypeVar
from dataclasses import dataclass, field
from enum import Enum
import time
from pydantic import BaseModel, Field
from omegaconf import DictConfig
from datetime import datetime


# Type variable for Pydantic models
T = TypeVar('T', bound=BaseModel)
    

class LaunchType(str, Enum):
    """EC2 instance launch type options."""
    SPOT = "SPOT"
    ON_DEMAND = "ON_DEMAND"
    
    @classmethod
    def from_string(cls, launch_type_str: str) -> 'LaunchType':
        """
        Convert a string launch type to the corresponding LaunchType enum value.
        
        Args:
            launch_type_str: Launch type string to convert
            
        Returns:
            LaunchType enum value
            
        Raises:
            ValueError: If launch type string is not valid
        """
        try:
            # Normalize input by converting to uppercase and replacing hyphens
            normalized_str = launch_type_str.upper().replace('-', '_')
            return cls(normalized_str)
        except ValueError:
            raise ValueError(f"Invalid launch type: {launch_type_str}. Valid values are: {[lt.value for lt in cls]}")
    

# =============================================================================
# DATA MODELS - CONFIGURATION
# =============================================================================
@dataclass
class NetworkConfig:
    """ECS task network configuration."""
    subnets: List[str]
    security_groups: List[str]
    assign_public_ip: str = 'DISABLED'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to AWS API compatible dictionary."""
        return {
            'awsvpcConfiguration': {
                'subnets': list(self.subnets),
                'securityGroups': list(self.security_groups),
                'assignPublicIp': self.assign_public_ip
            }
        }


class AutoscaleConfig(BaseModel):
    """Configuration for autoscaling parameters."""
    max_retries: int = Field(default=3, ge=0)
    retry_delay: int = Field(default=5, ge=1)
    initial_delay: int = Field(default=10, ge=1)
    scale_up_increment: int = Field(default=1, ge=1)
    max_wait_time: int = Field(default=600, ge=60)  # 10 minutes
    ecs_registration_timeout: int = Field(default=300, ge=60)  # 5 minutes
    instance_cleanup_threshold: int = Field(default=600, ge=60)  # 10 minutes
    aws_retry_attempts: int = Field(default=3, ge=1)
    aws_pool_connections: int = Field(default=10, ge=1)
    aws_timeout: int = Field(default=30, ge=5)
    max_consecutive_failures: int = Field(default=3, ge=1)

    @classmethod
    def from_dictconfig(cls, cfg: DictConfig) -> 'AutoscaleConfig':
        """
        Create configuration from OmegaConf DictConfig.
        
        Args:
            cfg: OmegaConf DictConfig containing aws.autoscale configuration
            
        Returns:
            AutoscaleConfig instance
            
        Raises:
            KeyError: If required configuration keys are missing
            TypeError: If configuration values have incorrect types
        """
        autoscale_cfg = cfg.aws.autoscale
        return cls(
            max_retries=autoscale_cfg.max_retries,
            retry_delay=autoscale_cfg.retry_delay,
            initial_delay=autoscale_cfg.initial_delay,
            scale_up_increment=autoscale_cfg.scale_up_increment,
            max_wait_time=autoscale_cfg.max_wait_time,
            ecs_registration_timeout=autoscale_cfg.ecs_registration_timeout,
            instance_cleanup_threshold=autoscale_cfg.instance_cleanup_threshold,
            aws_retry_attempts=autoscale_cfg.aws_retry_attempts,
            aws_pool_connections=autoscale_cfg.aws_pool_connections,
            aws_timeout=autoscale_cfg.aws_timeout,
            max_consecutive_failures=autoscale_cfg.get("max_consecutive_failures", 3)
        )
        
    @classmethod
    def from_opt(cls, opt: Dict) -> 'AutoscaleConfig':
        """
        Create configuration from OmegaConf DictConfig.
        
        Args:
            cfg: OmegaConf DictConfig containing aws.autoscale configuration
            
        Returns:
            AutoscaleConfig instance
            
        Raises:
            KeyError: If required configuration keys are missing
            TypeError: If configuration values have incorrect types
        """
        opt = add_attributes(["max_retries", 
                              "retry_delay", 
                              "initial_delay", 
                              "scale_up_increment", 
                              "max_wait_time", 
                              "ecs_registration_timeout", 
                              "instance_cleanup_threshold",
                              "aws_retry_attempts",
                              "aws_pool_connections",
                              "aws_timeout",
                              "max_consecutive_failures"
                              ], opt)
        return cls(
            max_retries=opt["max_retries"],
            retry_delay=opt["retry_delay"],
            initial_delay=opt["initial_delay"],
            scale_up_increment=opt["scale_up_increment"],
            max_wait_time=opt["max_wait_time"],
            ecs_registration_timeout=opt["ecs_registration_timeout"],
            instance_cleanup_threshold=opt["instance_cleanup_threshold"],
            aws_retry_attempts=opt["aws_retry_attempts"],
            aws_pool_connections=opt["aws_pool_connections"],
            aws_timeout=opt["aws_timeout"],
            max_consecutive_failures=opt.get("max_consecutive_failures", 3)
        )


# =============================================================================
# DATA MODELS - METRICS
# =============================================================================
class MetricsData(BaseModel):
    """Container for metrics data."""
    operation: str
    duration: float
    success: bool
    timestamp: float = Field(default_factory=time.time)
    state: str
    asg_name: str
    cluster_name: str
    instance_count: Optional[int] = None
    error_count: Optional[int] = None
    additional_data: Dict[str, Any] = Field(default_factory=dict)