"""
Example Django settings showing how to configure django-smart-storages.

This example demonstrates:
- Basic configuration for multiple buckets
- Using different storage backends for different purposes
- Multi-tenant setup
- Security-based bucket separation
"""

# AWS Credentials (shared across all buckets unless overridden)
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_S3_REGION_NAME = 'us-east-1'

# Example 1: Basic multi-bucket configuration
# Use different buckets for media, static, and document files
SMART_STORAGE_BUCKETS = {
    'media': {
        'bucket_name': 'myapp-media-bucket',
        'location': 'media/',
        'default_acl': 'public-read',
    },
    'static': {
        'bucket_name': 'myapp-static-bucket',
        'location': 'static/',
        'default_acl': 'public-read',
    },
    'documents': {
        'bucket_name': 'myapp-documents-bucket',
        'location': 'documents/',
        'default_acl': 'private',
    },
    'private': {
        'bucket_name': 'myapp-private-bucket',
        'location': 'private/',
        'default_acl': 'private',
    },
}

# Set default storage backends
DEFAULT_FILE_STORAGE = 'smart_storages.storages.MediaStorage'
STATICFILES_STORAGE = 'smart_storages.storages.StaticStorage'

# Example 2: Multi-tenant configuration
# Each tenant gets their own bucket
SMART_STORAGE_BUCKETS_MULTITENANT = {
    'tenant_acme': {
        'bucket_name': 'acme-corp-files',
        'location': '',
        'default_acl': 'private',
    },
    'tenant_globex': {
        'bucket_name': 'globex-corp-files',
        'location': '',
        'default_acl': 'private',
    },
    'tenant_initech': {
        'bucket_name': 'initech-files',
        'location': '',
        'default_acl': 'private',
    },
}

# Example 3: Security-based separation
# Different buckets for different security levels
SMART_STORAGE_BUCKETS_SECURITY = {
    'public': {
        'bucket_name': 'myapp-public-assets',
        'location': 'public/',
        'default_acl': 'public-read',
    },
    'internal': {
        'bucket_name': 'myapp-internal-files',
        'location': 'internal/',
        'default_acl': 'private',
    },
    'confidential': {
        'bucket_name': 'myapp-confidential-files',
        'location': 'confidential/',
        'default_acl': 'private',
        # Use a different region for compliance
        'region_name': 'eu-west-1',
    },
    'pii': {
        'bucket_name': 'myapp-pii-data',
        'location': 'pii/',
        'default_acl': 'private',
        # Use dedicated credentials with limited permissions
        'access_key': 'pii-specific-access-key',
        'secret_key': 'pii-specific-secret-key',
        'region_name': 'us-gov-west-1',
    },
}

# Example 4: Environment-based configuration
# Different buckets for different environments
import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

SMART_STORAGE_BUCKETS_ENV = {
    'media': {
        'bucket_name': f'myapp-{ENVIRONMENT}-media',
        'location': 'media/',
        'default_acl': 'public-read' if ENVIRONMENT == 'production' else 'private',
    },
    'static': {
        'bucket_name': f'myapp-{ENVIRONMENT}-static',
        'location': 'static/',
        'default_acl': 'public-read',
    },
}
