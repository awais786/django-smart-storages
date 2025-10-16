"""Utilities for creating custom storage backends."""
from .storages import SmartS3Storage


def create_storage_class(module_name, **default_settings):
    """
    Factory function to create a custom storage class for a specific module.
    
    Args:
        module_name (str): The name of the module
        **default_settings: Default settings for the storage class
        
    Returns:
        class: A new storage class configured for the module
        
    Example:
        >>> CustomStorage = create_storage_class(
        ...     'uploads',
        ...     location='uploads',
        ...     default_acl='private',
        ...     file_overwrite=False
        ... )
        >>> storage = CustomStorage()
    """
    class CustomStorage(SmartS3Storage):
        """Custom storage class created dynamically."""
        pass
    
    CustomStorage.module_name = module_name
    CustomStorage.__name__ = f"{module_name.capitalize()}Storage"
    
    # Store default settings
    original_init = CustomStorage.__init__
    
    def __init__(self, **settings_override):
        # Merge default_settings with settings_override
        merged_settings = {**default_settings, **settings_override}
        original_init(self, **merged_settings)
    
    CustomStorage.__init__ = __init__
    
    return CustomStorage
