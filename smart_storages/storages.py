"""Storage backends with multi-bucket support."""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from .config import get_bucket_config, get_default_bucket_config


class SmartS3Storage(S3Boto3Storage):
    """
    Base S3 storage class with smart bucket selection.
    
    This class extends django-storages S3Boto3Storage to support
    different buckets for different modules.
    """
    
    module_name = None  # Should be overridden in subclasses
    
    def __init__(self, **settings_override):
        """Initialize storage with module-specific bucket configuration."""
        # Get module-specific configuration
        if self.module_name:
            module_config = get_bucket_config(self.module_name)
        else:
            module_config = get_default_bucket_config()
        
        # Override settings with module-specific config
        settings_override.setdefault('bucket_name', module_config.get('bucket_name'))
        settings_override.setdefault('location', module_config.get('location', ''))
        settings_override.setdefault('default_acl', module_config.get('default_acl'))
        settings_override.setdefault('access_key', module_config.get('access_key'))
        settings_override.setdefault('secret_key', module_config.get('secret_key'))
        settings_override.setdefault('region_name', module_config.get('region_name'))
        
        # Only remove None values for keys that shouldn't be passed as None
        # Keep None for optional parameters like default_acl which might be intentionally None
        filtered_settings = {}
        for key, value in settings_override.items():
            # Only include non-None values, but keep empty strings
            if value is not None:
                filtered_settings[key] = value
        
        super().__init__(**filtered_settings)


class MediaStorage(SmartS3Storage):
    """Storage backend for media files."""
    
    module_name = 'media'
    
    def __init__(self, **settings_override):
        """Initialize media storage."""
        settings_override.setdefault('location', 'media')
        settings_override.setdefault('file_overwrite', False)
        super().__init__(**settings_override)


class StaticStorage(SmartS3Storage):
    """Storage backend for static files."""
    
    module_name = 'static'
    
    def __init__(self, **settings_override):
        """Initialize static storage."""
        settings_override.setdefault('location', 'static')
        super().__init__(**settings_override)


class DocumentStorage(SmartS3Storage):
    """Storage backend for document files."""
    
    module_name = 'documents'
    
    def __init__(self, **settings_override):
        """Initialize document storage."""
        settings_override.setdefault('location', 'documents')
        settings_override.setdefault('default_acl', 'private')
        settings_override.setdefault('file_overwrite', False)
        super().__init__(**settings_override)


class PrivateStorage(SmartS3Storage):
    """Storage backend for private files."""
    
    module_name = 'private'
    
    def __init__(self, **settings_override):
        """Initialize private storage."""
        settings_override.setdefault('location', 'private')
        settings_override.setdefault('default_acl', 'private')
        settings_override.setdefault('file_overwrite', False)
        super().__init__(**settings_override)


class PublicStorage(SmartS3Storage):
    """Storage backend for public files."""
    
    module_name = 'public'
    
    def __init__(self, **settings_override):
        """Initialize public storage."""
        settings_override.setdefault('location', 'public')
        settings_override.setdefault('default_acl', 'public-read')
        super().__init__(**settings_override)
