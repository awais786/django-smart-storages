from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting


class BaseSpecialS3Storage(S3Boto3Storage):
    """
    Generic reusable S3 storage backend.
    Uses the bucket defined by a Django setting key.
    """

    storage_key = None  # e.g. "import_export" or "COURSE_IMPORT_EXPORT_BUCKET"

    def __init__(self, **kwargs):
        # Start with sane defaults
        options = {"querystring_auth": True}

        # Load from STORAGES if configured
        if hasattr(settings, "STORAGES") and self.storage_key:
            storage_conf = settings.STORAGES.get(self.storage_key, {})
            options.update(storage_conf.get("OPTIONS", {}))

        # Fallback: if bucket not set, look for setting variable
        if "bucket_name" not in options:
            # Allow storage_key to be either "import_export"
            bucket_name = getattr(settings, self.storage_key, None)
            if not bucket_name:
                bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
            options["bucket_name"] = bucket_name

        #  Finally, user kwargs override everything
        options.update(kwargs)

        super().__init__(**options)
