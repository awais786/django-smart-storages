# django-smart-storages

Reusable, specialized storage backends built on top of django-storages

This package provides a simple, consistent way to define multiple custom S3 or file storage backends in Django projects — each with its own configuration, bucket, or logic — without repeating boilerplate code.

# Features

Clean abstraction for per-use-case S3 buckets
Seamless integration with django-storages
Built-in backend resolver for dynamic imports
Optional fallback to local storage in development
Easy to extend for any specialized storage use case

# Installation

`pip install django-special-storages`

# Configuration

In your Django settings, add the relevant apps:

```python
# settings.py

INSTALLED_APPS = [
    'storages',    # this is for django-storages
]
```
## Example: Custom Storage Classes

Define specialized storage classes in your code (e.g., `views.py` or a separate `storages.py`):

```python
# views.py (or storages.py)

from smart_storages import BaseSpecialS3Storage

class ImportExportS3Storage(BaseSpecialS3Storage):
    storage_key = "import_export"

class AnalyticsS3Storage(BaseSpecialS3Storage):
    storage_key = "analytics"
```


## Example: Configuring Multiple Storages

Add your bucket names and the STORAGES setting:

```python
# settings.py

AWS_STORAGE_BUCKET_NAME = "main-bucket"

STORAGES = {
    # Default file storage
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    # Static files
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },

    # Import-export-specific S3 storage (using your custom base class)
    "import_export": {
        "BACKEND": "special_storages.s3.ImportExportS3Storage",
        "OPTIONS": {
            "custom_domain": None,
            "querystring_auth": True,
        },
    },

    # Analytics-specific S3 storage
    "analytics": {
        "BACKEND": "special_storages.s3.AnalyticsS3Storage",
        "OPTIONS": {
            "custom_domain": None,
        },
    },
}
```

## Example: Usage

```
# it will save the image in given bucket.
class PublicImage(models.Model):
    file = models.FileField(storage=ImportExportS3())


```



> **Note:**  
> You can place these custom storage classes in any appropriate module (such as `storages.py`), and reference them in your `STORAGES` Django setting.
