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

AWS_STORAGE_BUCKET_NAME = "main-bucket"
COURSE_IMPORT_EXPORT_BUCKET = "import-export-bucket"

SPECIAL_STORAGES = {
    "import_export": "special_storages.s3.ImportExportS3Storage",
    "analytics": "special_storages.s3.AnalyticsS3Storage",
}
