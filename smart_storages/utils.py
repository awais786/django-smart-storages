"""Utilities for creating custom storage backends."""
import re
from .storages import SmartS3Storage


def create_storage_class(module_name, **default_settings):
    """
    Factory function to create a custom storage class for a specific module.
    
    Args:
        module_name (str): The name of the module (must be a valid Python identifier)
        **default_settings: Default settings for the storage class
        
    Returns:
        class: A new storage class configured for the module
        
    Raises:
        ValueError: If module_name is not a valid identifier
        
    Example:
        >>> CustomStorage = create_storage_class(
        ...     'uploads',
        ...     location='uploads',
        ...     default_acl='private',
        ...     file_overwrite=False
        ... )
        >>> storage = CustomStorage()
    """
    # Validate module_name is a valid identifier (or can be made into one)
    if not module_name:
        raise ValueError("module_name cannot be empty")
    
    # Sanitize module_name for use in class name
    # Replace non-alphanumeric characters with underscores
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', module_name)
    # Ensure it doesn't start with a digit
    if sanitized_name[0].isdigit():
        sanitized_name = '_' + sanitized_name
    
    class CustomStorage(SmartS3Storage):
        """Custom storage class created dynamically."""
        pass
    
    CustomStorage.module_name = module_name
    CustomStorage.__name__ = f"{sanitized_name.capitalize()}Storage"
    
    # Store default settings
    original_init = CustomStorage.__init__
    
    def __init__(self, **settings_override):
        # Merge default_settings with settings_override
        merged_settings = {**default_settings, **settings_override}
        original_init(self, **merged_settings)
    
    CustomStorage.__init__ = __init__
    
    return CustomStorage
