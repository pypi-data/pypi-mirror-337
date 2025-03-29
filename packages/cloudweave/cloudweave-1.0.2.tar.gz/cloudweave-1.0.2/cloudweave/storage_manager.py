import enum
import json
import os
import uuid
from typing import Dict, Any, Optional, List, Union, BinaryIO
from threading import Lock

# Import the Logger directly (using LOCAL type only)
from cloudweave.logging_manager import Logger, LoggerType

class StorageType(enum.Enum):
    """Enum for supported storage types."""
    S3 = "s3"
    GCS = "gcs"
    
    @classmethod
    def from_string(cls, value: str) -> 'StorageType':
        """Convert string to enum value."""
        try:
            return cls(value.lower())
        except ValueError:
            valid_values = ', '.join([e.value for e in cls])
            raise ValueError(f"Invalid storage type: {value}. Valid values are: {valid_values}")


class Storage:
    """
    Unified storage interface that can connect to multiple cloud storage backends.
    Supports maintaining multiple connections to different storage types simultaneously.
    """
    
    # Registry of storage instances
    _registry = {}
    _lock = Lock()
    
    def __init__(self, 
                storage_type: Union[str, StorageType],
                namespace: str,
                instance_id: Optional[str] = None,
                logger_instance: Optional[Logger] = None,
                **kwargs):
        """
        Initialize a storage connection.
        
        Args:
            storage_type: Type of storage to connect to (s3 or gcs)
            namespace: Namespace prefix for buckets/folders
            instance_id: Optional unique identifier for this connection
            logger_instance: Optional logger instance to use
            **kwargs: Storage-specific connection parameters
        """
        # Convert string to enum if necessary
        if isinstance(storage_type, str):
            self.storage_type = StorageType.from_string(storage_type)
        else:
            self.storage_type = storage_type
            
        self.namespace = namespace
        
        # Generate unique instance ID if not provided
        self.instance_id = instance_id or f"{self.storage_type.value}-{namespace}-{uuid.uuid4()}"
        
        # Set up logger (create a LOCAL logger if not provided)
        if logger_instance is None:
            self.logger = Logger(
                logger_type=LoggerType.LOCAL,
                namespace=f"storage-{self.namespace}",
                instance_id=f"logger-{self.instance_id}",
                log_level=kwargs.get('log_level', 'info')
            )
        else:
            self.logger = logger_instance
        
        self._storage_manager = None
        self._default_bucket = kwargs.get('default_bucket')
        
        # Set up storage connection
        self._setup_storage(**kwargs)
        
        # Register this instance
        with Storage._lock:
            Storage._registry[self.instance_id] = self
    
    @classmethod
    def get_instance(cls, instance_id: str) -> Optional['Storage']:
        """
        Get a storage instance by ID.
        
        Args:
            instance_id: Storage instance ID
            
        Returns:
            Storage instance or None if not found
        """
        return cls._registry.get(instance_id)
        
    @classmethod
    def list_instances(cls) -> List[str]:
        """
        List all registered storage instance IDs.
        
        Returns:
            List of instance IDs
        """
        return list(cls._registry.keys())
    
    def _setup_storage(self, **kwargs):
        """
        Initialize the storage connection based on the storage type.
        
        Args:
            **kwargs: Storage-specific connection parameters
        """
        if self.storage_type == StorageType.S3:
            self._setup_s3(**kwargs)
        elif self.storage_type == StorageType.GCS:
            self._setup_gcs(**kwargs)
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")
    
    def _setup_s3(self, **kwargs):
        """
        Initialize S3 connection.
        
        Args:
            **kwargs: Additional S3-specific parameters
        """
        from cloudweave.storage_utils import S3Manager
        
        self._storage_manager = S3Manager(kwargs)
        self.logger.info(f"S3 connection initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def _setup_gcs(self, **kwargs):
        """
        Initialize GCS connection.
        
        Args:
            **kwargs: Additional GCS-specific parameters
        """
        from cloudweave.storage_utils import StorageManager
        
        self._storage_manager = StorageManager(kwargs)
        self.logger.info(f"GCS connection initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def get_native_manager(self):
        """
        Get the native storage manager instance.
        
        Returns:
            The underlying storage manager (S3Manager or StorageManager)
        """
        return self._storage_manager
    
    def _get_bucket(self, bucket_name: Optional[str] = None) -> str:
        """
        Get the bucket name, using default if not provided.
        
        Args:
            bucket_name: Optional bucket name
            
        Returns:
            Bucket name to use
            
        Raises:
            ValueError: If no bucket name is provided and no default is set
        """
        if bucket_name:
            return bucket_name
        elif self._default_bucket:
            return self._default_bucket
        else:
            raise ValueError("No bucket name provided and no default bucket set")
    
    def download_file(self, bucket_name: Optional[str], source_path: str, local_path: str) -> bool:
        """
        Download a file from cloud storage to a local destination.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            source_path: Source file path in cloud storage
            local_path: Local destination file path
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Downloading file from {bucket}/{source_path} to {local_path}")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.download_file(bucket, source_path, local_path)
            else:  # GCS
                result = self._storage_manager.download_file(bucket, source_path, local_path)
                
            if result:
                self.logger.info(f"Successfully downloaded file from {bucket}/{source_path}")
            else:
                self.logger.error(f"Failed to download file from {bucket}/{source_path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error downloading file from {bucket}/{source_path}: {e}")
            return False
    
    def upload_file(self, local_path: str, bucket_name: Optional[str], dest_path: str, 
                   content_type: Optional[str] = None) -> bool:
        """
        Upload a file to cloud storage.
        
        Args:
            local_path: Local file path
            bucket_name: Storage bucket name (optional if default bucket is set)
            dest_path: Destination path in cloud storage
            content_type: Optional content type
            
        Returns:
            bool: True if upload was successful, False otherwise
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Uploading file from {local_path} to {bucket}/{dest_path}")
        
        try:
            if self.storage_type == StorageType.S3:
                extra_args = {}
                if content_type:
                    extra_args['ContentType'] = content_type
                result = self._storage_manager.upload_file(local_path, bucket, dest_path, extra_args)
            else:  # GCS
                result = self._storage_manager.upload_file(local_path, bucket, dest_path, content_type)
                
            if result:
                self.logger.info(f"Successfully uploaded file to {bucket}/{dest_path}")
            else:
                self.logger.error(f"Failed to upload file to {bucket}/{dest_path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error uploading file to {bucket}/{dest_path}: {e}")
            return False
    

    def read_file(self, bucket_name: Optional[str], path: str, decode: bool = True) -> Optional[Union[str, bytes]]:
        """
        Read file content from cloud storage directly into a variable.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            path: Path to file in cloud storage
            decode: Whether to decode the content as UTF-8 (for text files)
            
        Returns:
            File content as string or bytes, or None if operation failed
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Reading file from {bucket}/{path}")
        
        try:
            if self.storage_type == StorageType.S3:
                content = self._storage_manager.read_file(bucket, path, decode)
            else:  # GCS
                content = self._storage_manager.read_file(bucket, path, decode)
                
            if content is not None:
                content_type = "text" if decode else "binary"
                content_size = len(content)
                self.logger.info(f"Successfully read {content_size} bytes of {content_type} data from {bucket}/{path}")
            else:
                self.logger.error(f"Failed to read file from {bucket}/{path}")
                
            return content
        except Exception as e:
            self.logger.error(f"Error reading file from {bucket}/{path}: {e}")
            return None
        
    def write_file(self, content: Union[str, bytes], bucket_name: Optional[str], dest_path: str, 
                content_type: Optional[str] = None) -> bool:
        """
        Write content directly to a file in cloud storage.
        
        Args:
            content: Content to write (string or bytes)
            bucket_name: Storage bucket name (optional if default bucket is set)
            dest_path: Destination path in cloud storage
            content_type: Optional content type
            
        Returns:
            bool: True if write was successful, False otherwise
        """
        bucket = self._get_bucket(bucket_name)
        content_size = len(content)
        content_type_str = "text" if isinstance(content, str) else "binary"
        self.logger.info(f"Writing {content_size} bytes of {content_type_str} data to {bucket}/{dest_path}")
        
        try:
            # Convert string to bytes if needed
            if isinstance(content, str):
                content = content.encode('utf-8')
                
            if self.storage_type == StorageType.S3:
                extra_args = {}
                if content_type:
                    extra_args['ContentType'] = content_type
                result = self._storage_manager.write_file(bucket, dest_path, content, extra_args)
            else:  # GCS
                result = self._storage_manager.write_file(bucket, dest_path, content, content_type)
                
            if result:
                self.logger.info(f"Successfully wrote data to {bucket}/{dest_path}")
            else:
                self.logger.error(f"Failed to write data to {bucket}/{dest_path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error writing data to {bucket}/{dest_path}: {e}")
            return False

    def delete_file(self, bucket_name: Optional[str], path: str) -> bool:
        """
        Delete a file from cloud storage.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            path: Path to file in cloud storage
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Deleting file from {bucket}/{path}")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.delete_file(bucket, path)
            else:  # GCS
                result = self._storage_manager.delete_file(bucket, path)
                
            if result:
                self.logger.info(f"Successfully deleted file from {bucket}/{path}")
            else:
                self.logger.error(f"Failed to delete file from {bucket}/{path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error deleting file from {bucket}/{path}: {e}")
            return False

    def list_files(self, bucket_name: Optional[str], prefix: str = "", 
                delimiter: str = "/", max_results: Optional[int] = None) -> Optional[List[str]]:
        """
        List files in a bucket with the given prefix.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            prefix: Prefix to filter by
            delimiter: Delimiter for hierarchical listing
            max_results: Maximum number of results to return
            
        Returns:
            List of file paths or None if operation failed
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Listing files in {bucket} with prefix '{prefix}'")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.list_files(bucket, prefix, delimiter, max_results)
            else:  # GCS
                result = self._storage_manager.list_files(bucket, prefix, delimiter, max_results)
                
            if result is not None:
                self.logger.info(f"Found {len(result)} files in {bucket} with prefix '{prefix}'")
            else:
                self.logger.error(f"Failed to list files in {bucket} with prefix '{prefix}'")
                
            return result
        except Exception as e:
            self.logger.error(f"Error listing files in {bucket} with prefix '{prefix}': {e}")
            return None

    def get_file_metadata(self, bucket_name: Optional[str], path: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a file in cloud storage.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            path: Path to file in cloud storage
            
        Returns:
            Dict with metadata or None if operation failed
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Getting metadata for {bucket}/{path}")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.get_file_metadata(bucket, path)
            else:  # GCS
                result = self._storage_manager.get_file_metadata(bucket, path)
                
            if result is not None:
                self.logger.info(f"Successfully retrieved metadata for {bucket}/{path}")
            else:
                self.logger.error(f"Failed to retrieve metadata for {bucket}/{path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error retrieving metadata for {bucket}/{path}: {e}")
            return None

    def file_exists(self, bucket_name: Optional[str], path: str) -> bool:
        """
        Check if a file exists in cloud storage.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            path: Path to file in cloud storage
            
        Returns:
            bool: True if file exists, False otherwise
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Checking if file exists: {bucket}/{path}")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.file_exists(bucket, path)
            else:  # GCS
                result = self._storage_manager.file_exists(bucket, path)
                
            self.logger.info(f"File {bucket}/{path} exists: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error checking if file exists {bucket}/{path}: {e}")
            return False

    def copy_file(self, source_bucket: Optional[str], source_path: str, 
                dest_bucket: Optional[str], dest_path: str) -> bool:
        """
        Copy a file within cloud storage.
        
        Args:
            source_bucket: Source bucket name (optional if default bucket is set)
            source_path: Source file path
            dest_bucket: Destination bucket name (optional if default bucket is set)
            dest_path: Destination file path
            
        Returns:
            bool: True if copy was successful, False otherwise
        """
        source_bucket = self._get_bucket(source_bucket)
        dest_bucket = self._get_bucket(dest_bucket)
        
        self.logger.info(f"Copying file from {source_bucket}/{source_path} to {dest_bucket}/{dest_path}")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.copy_file(source_bucket, source_path, dest_bucket, dest_path)
            else:  # GCS
                result = self._storage_manager.copy_file(source_bucket, source_path, dest_bucket, dest_path)
                
            if result:
                self.logger.info(f"Successfully copied file from {source_bucket}/{source_path} to {dest_bucket}/{dest_path}")
            else:
                self.logger.error(f"Failed to copy file from {source_bucket}/{source_path} to {dest_bucket}/{dest_path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error copying file from {source_bucket}/{source_path} to {dest_bucket}/{dest_path}: {e}")
            return False

    def create_folder(self, bucket_name: Optional[str], folder_path: str) -> bool:
        """
        Create a folder/prefix in cloud storage.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            folder_path: Folder path to create (should end with '/')
            
        Returns:
            bool: True if creation was successful, False otherwise
        """
        bucket = self._get_bucket(bucket_name)
        # Ensure path ends with '/'
        if not folder_path.endswith('/'):
            folder_path = folder_path + '/'
            
        self.logger.info(f"Creating folder {bucket}/{folder_path}")
        
        try:
            if self.storage_type == StorageType.S3:
                result = self._storage_manager.write_file(bucket, folder_path, b'', {})
            else:  # GCS
                result = self._storage_manager.write_file(bucket, folder_path, b'', None)
                
            if result:
                self.logger.info(f"Successfully created folder {bucket}/{folder_path}")
            else:
                self.logger.error(f"Failed to create folder {bucket}/{folder_path}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error creating folder {bucket}/{folder_path}: {e}")
            return False

    def generate_signed_url(self, bucket_name: Optional[str], path: str, 
                        expiration: int = 3600, method: str = 'GET') -> Optional[str]:
        """
        Generate a signed URL for accessing a file.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            path: Path to file in cloud storage
            expiration: URL expiration time in seconds (default: 1 hour)
            method: HTTP method ('GET', 'PUT', etc.)
            
        Returns:
            Signed URL as string or None if operation failed
        """
        bucket = self._get_bucket(bucket_name)
        self.logger.info(f"Generating signed URL for {bucket}/{path} (method: {method}, expiration: {expiration}s)")
        
        try:
            if self.storage_type == StorageType.S3:
                signed_url = self._storage_manager.generate_signed_url(bucket, path, expiration, method)
            else:  # GCS
                signed_url = self._storage_manager.generate_signed_url(bucket, path, expiration, method)
                
            if signed_url:
                self.logger.info(f"Successfully generated signed URL for {bucket}/{path}")
            else:
                self.logger.error(f"Failed to generate signed URL for {bucket}/{path}")
                
            return signed_url
        except Exception as e:
            self.logger.error(f"Error generating signed URL for {bucket}/{path}: {e}")
            return None

    def save_json(self, data: Dict[str, Any], bucket_name: Optional[str], dest_path: str) -> bool:
        """
        Save JSON-serializable data to cloud storage.
        
        Args:
            data: JSON-serializable data
            bucket_name: Storage bucket name (optional if default bucket is set)
            dest_path: Destination path in cloud storage
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            import json
            json_data = json.dumps(data)
            return self.write_file(json_data, bucket_name, dest_path, 'application/json')
        except Exception as e:
            self.logger.error(f"Error saving JSON data: {e}")
            return False

    def load_json(self, bucket_name: Optional[str], path: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from cloud storage.
        
        Args:
            bucket_name: Storage bucket name (optional if default bucket is set)
            path: Path to JSON file in cloud storage
            
        Returns:
            Parsed JSON data or None if operation failed
        """
        try:
            import json
            content = self.read_file(bucket_name, path)
            if content is None:
                return None
            return json.loads(content)
        except Exception as e:
            self.logger.error(f"Error loading JSON data: {e}")
            return None

    def close(self):
        """
        Close the storage connection and clean up resources.
        """
        self.logger.info(f"Closing storage connection for {self.instance_id}")
        
        # Remove from registry
        with Storage._lock:
            if self.instance_id in Storage._registry:
                del Storage._registry[self.instance_id]
        
        # Close the underlying manager if it has a close method
        if hasattr(self._storage_manager, 'close') and callable(self._storage_manager.close):
            try:
                self._storage_manager.close()
            except Exception as e:
                self.logger.error(f"Error closing storage manager: {e}")
            


# Example usage
def create_storage_with_logger(
    storage_type: str,
    namespace: str,
    instance_id: Optional[str] = None,
    **kwargs
) -> Storage:
    """
    Create a Storage instance with a dedicated Logger.
    
    Args:
        storage_type: Type of storage to connect to (s3 or gcs)
        namespace: Namespace prefix for buckets/folders
        instance_id: Optional unique identifier for this connection
        **kwargs: Storage-specific connection parameters
        
    Returns:
        Storage instance with attached Logger
    """
    # Create a LOCAL logger first
    logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace=f"storage-{namespace}",
        instance_id=f"logger-{instance_id or uuid.uuid4()}",
        log_level=kwargs.get('log_level', 'info')
    )
    
    # Create the Storage instance with this logger
    return Storage(
        storage_type=storage_type,
        namespace=namespace,
        instance_id=instance_id,
        logger_instance=logger,
        **kwargs
    )
