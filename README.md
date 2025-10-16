# django-smart-storages

A Django plugin built on top of django-storages that provides functionality to use different S3 buckets for different modules in your Django application.

## Features

- **Multi-bucket support**: Use different S3 buckets for different purposes (media, static, documents, etc.)
- **Easy configuration**: Simple dictionary-based configuration in Django settings
- **Pre-configured storage backends**: Ready-to-use storage classes for common use cases
- **Custom storage creation**: Factory function to create custom storage backends
- **Built on django-storages**: Leverages the robust django-storages S3 backend

## Installation

```bash
pip install django-smart-storages
```

Or install from source:

```bash
pip install -e .
```

## Quick Start

1. Add `smart_storages` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'smart_storages',
]
```

2. Configure your buckets in `settings.py`:

```python
# AWS credentials (shared across all buckets)
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_S3_REGION_NAME = 'us-east-1'

# Smart storage bucket configuration
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
    'private': {
        'bucket_name': 'my-private-bucket',
        'location': 'private/',
        'default_acl': 'private',
    },
}
```

3. Use the storage backends in your models or settings:

```python
from smart_storages.storages import MediaStorage, DocumentStorage

# In your models
from django.db import models

class MyModel(models.Model):
    image = models.ImageField(storage=MediaStorage())
    document = models.FileField(storage=DocumentStorage())

# Or in settings for default storage
DEFAULT_FILE_STORAGE = 'smart_storages.storages.MediaStorage'
STATICFILES_STORAGE = 'smart_storages.storages.StaticStorage'
```

## Available Storage Backends

### Pre-configured Backends

- **MediaStorage**: For media files (default location: `media/`, default ACL: inherited from config)
- **StaticStorage**: For static files (default location: `static/`)
- **DocumentStorage**: For document files (default location: `documents/`, default ACL: `private`)
- **PrivateStorage**: For private files (default location: `private/`, default ACL: `private`)
- **PublicStorage**: For public files (default location: `public/`, default ACL: `public-read`)

### Creating Custom Storage Backends

You can create custom storage backends using the factory function:

```python
from smart_storages.utils import create_storage_class

# Create a custom storage for uploads
UploadStorage = create_storage_class(
    'uploads',
    location='uploads',
    default_acl='private',
    file_overwrite=False
)

# Use it in your model
class MyModel(models.Model):
    upload = models.FileField(storage=UploadStorage())
```

Or by subclassing `SmartS3Storage`:

```python
from smart_storages.storages import SmartS3Storage

class CustomStorage(SmartS3Storage):
    module_name = 'custom'
    
    def __init__(self, **settings_override):
        settings_override.setdefault('location', 'custom')
        settings_override.setdefault('default_acl', 'private')
        super().__init__(**settings_override)
```

## Configuration

### Bucket Configuration

Each module in `SMART_STORAGE_BUCKETS` can have the following settings:

- `bucket_name`: The name of the S3 bucket (required)
- `location`: The path prefix within the bucket (optional, default: '')
- `default_acl`: The default ACL for files (optional, e.g., 'public-read', 'private')
- `access_key`: Module-specific AWS access key (optional, falls back to global settings)
- `secret_key`: Module-specific AWS secret key (optional, falls back to global settings)
- `region_name`: Module-specific AWS region (optional, falls back to global settings)

### Fallback Behavior

If a module is not configured in `SMART_STORAGE_BUCKETS`, it will fall back to the default AWS settings:

```python
AWS_STORAGE_BUCKET_NAME = 'default-bucket'
AWS_LOCATION = ''
AWS_DEFAULT_ACL = None
```

## Use Cases

### Separating Media and Static Files

```python
SMART_STORAGE_BUCKETS = {
    'media': {
        'bucket_name': 'myapp-media',
        'location': 'media/',
    },
    'static': {
        'bucket_name': 'myapp-static',
        'location': 'static/',
    },
}

DEFAULT_FILE_STORAGE = 'smart_storages.storages.MediaStorage'
STATICFILES_STORAGE = 'smart_storages.storages.StaticStorage'
```

### Multi-tenant Applications

```python
# Use different buckets for different tenants
SMART_STORAGE_BUCKETS = {
    'tenant_a': {
        'bucket_name': 'tenant-a-files',
    },
    'tenant_b': {
        'bucket_name': 'tenant-b-files',
    },
}
```

### Compliance and Security

```python
# Separate buckets for different security levels
SMART_STORAGE_BUCKETS = {
    'public': {
        'bucket_name': 'myapp-public',
        'default_acl': 'public-read',
    },
    'private': {
        'bucket_name': 'myapp-private',
        'default_acl': 'private',
    },
    'sensitive': {
        'bucket_name': 'myapp-sensitive',
        'default_acl': 'private',
        'region_name': 'us-gov-west-1',  # Government cloud
    },
}
```

## Requirements

- Python >= 3.8
- Django >= 3.2
- django-storages >= 1.12
- boto3 >= 1.20

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.