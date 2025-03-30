class AutoscaleError(Exception):
    """Base class for autoscaling errors."""
    pass

class InstanceError(AutoscaleError):
    """Error related to EC2 instance operations."""
    pass

class ECSError(AutoscaleError):
    """Error related to ECS operations."""
    pass

class ASGError(AutoscaleError):
    """Error related to AutoScaling Group operations."""
    pass

class InstanceGroupError(AutoscaleError):
    """Error related to ECS operations."""
    pass

class ComputeError(AutoscaleError):
    """Error related to AutoScaling Group operations."""
    pass


class TimeoutError(AutoscaleError):
    """Error related to operation timeouts."""
    pass