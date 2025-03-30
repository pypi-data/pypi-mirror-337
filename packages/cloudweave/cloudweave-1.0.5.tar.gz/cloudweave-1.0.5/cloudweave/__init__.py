# multicloud_utils/__init__.py
from cloudweave.auth_manager import get_auth_manager, CloudWeaveAuthManager, AuthenticationError
from cloudweave.database_manager import DatabaseType
from cloudweave.logging_manager import LoggerType
from cloudweave.storage_manager import StorageType
from cloudweave.autoscale_manager import CloudProviderType
from cloudweave.metadata import __version__, __author__, __email__, __description__

# non authenticated classes
from cloudweave.cloud_session_utils import GCPManager, AWSManager
from cloudweave.secret_utils import (
    AWSSecretsStore, 
    GCPSecretsStore,
    SecretAccessError, 
    SecretConversionError, 
    SecretNotFoundError, 
    SecretsStoreError, 
    SecretType
)
# Expose only authenticated interfaces
__all__ = [
    'get_auth_manager',
    'CloudWeaveAuthManager',
    'AuthenticationError',
    'DatabaseType',
    'LoggerType',
    'StorageType',
    'GCPManager',
    'AWSManager',
    'AWSSecretsStore',
    'GCPSecretsStore',
    'CloudProviderType',
    'SecretType',
    'SecretAccessError',
    'SecretConversionError',
    'SecretNotFoundError',
    'SecretsStoreError',
    
]

# Optional convenience function for quick setup
def init_auth(api_key: str):
    """Quick initialization of the authentication manager with the given API key."""
    return get_auth_manager(api_key)