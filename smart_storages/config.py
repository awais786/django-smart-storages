"""Configuration utilities for smart storages."""
from django.conf import settings


def get_bucket_config(module_name):
    """
    Get bucket configuration for a specific module.
    
    Args:
        module_name (str): The name of the module (e.g., 'media', 'static', 'documents')
        
    Returns:
        dict: Configuration dictionary for the module including bucket name and other settings
        
    Example settings in Django settings.py:
        SMART_STORAGE_BUCKETS = {
            'media': {
                'bucket_name': 'my-media-bucket',
                'location': 'media/',
                'default_acl': 'public-read',
            },
            'static': {
                'bucket_name': 'my-static-bucket',
                'location': 'static/',
                'default_acl': 'public-read',
            },
            'documents': {
                'bucket_name': 'my-documents-bucket',
                'location': 'documents/',
                'default_acl': 'private',
            },
        }
    """
    buckets_config = getattr(settings, 'SMART_STORAGE_BUCKETS', {})
    
    if module_name not in buckets_config:
        # Fall back to default AWS settings if module not configured
        return {
            'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
            'location': getattr(settings, 'AWS_LOCATION', ''),
            'default_acl': getattr(settings, 'AWS_DEFAULT_ACL', None),
        }
    
    return buckets_config[module_name]


def get_default_bucket_config():
    """
    Get default bucket configuration.
    
    Returns:
        dict: Default configuration dictionary
    """
    return {
        'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
        'location': getattr(settings, 'AWS_LOCATION', ''),
        'default_acl': getattr(settings, 'AWS_DEFAULT_ACL', None),
        'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
        'secret_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
        'region_name': getattr(settings, 'AWS_S3_REGION_NAME', None),
    }
