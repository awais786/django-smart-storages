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

In your Django settings:

INSTALLED_APPS = [

    'storages',
    'special_storages',
]


# example
# settings.py

```
AWS_STORAGE_BUCKET_NAME = "main-bucket"
COURSE_IMPORT_EXPORT_BUCKET = "import-export-bucket"

STORAGES = {
    # Default file storage
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    # Static files
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },

    # Import/export-specific S3 storage (using your custom base class)
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

views.py

from django.conf import settings
from special_storages.base import BaseSpecialS3Storage

class ImportExportS3Storage(BaseSpecialS3Storage):
    setting_name = "COURSE_IMPORT_EXPORT_BUCKET"


class AnalyticsS3Storage(BaseSpecialS3Storage):
    setting_name = "ANALYTICS_BUCKET"

```


