from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class BaseSpecialS3Storage(S3Boto3Storage):
    """
    Generic reusable S3 storage backend.
    Uses the bucket defined by a Django setting key.
    """

    storage_key = None  # e.g. "import_export" or "COURSE_IMPORT_EXPORT_BUCKET"

    def __init__(self, **kwargs):
        # Start with sane defaults
        options = {"querystring_auth": True}
        bucket_name = None
        
        # 1. Try STORAGES dict
        if hasattr(settings, "STORAGES") and self.storage_key:
            storage_conf = settings.STORAGES.get(self.storage_key, {})
            options.update(storage_conf.get("OPTIONS", {}))
            bucket_name = options.get("bucket_name", None)

        # 2. Fallback to storage_key setting if bucket_name is None
        if bucket_name is None and self.storage_key:
            bucket_name = getattr(settings, self.storage_key, None)

        # 3. Final fallback to AWS_STORAGE_BUCKET_NAME if still None
        if bucket_name is None:
            bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)

        options["bucket_name"] = bucket_name

        # 4. Override with any kwargs
        options.update(kwargs)

        super().__init__(**options)
