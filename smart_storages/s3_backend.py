from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting


class BaseSpecialS3Storage(S3Boto3Storage):
    """
    Generic reusable S3 storage backend.
    Uses the bucket defined by a Django setting key.
    """

    setting_name = None  # subclasses must define this

    def __init__(self, **kwargs):
        # Explicitly resolve bucket name from Django settings or fallback
        if self.setting_name and hasattr(settings, self.setting_name):
            bucket_name = getattr(settings, self.setting_name)
        else:
            bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
        # Merge default options with user-supplied ones
        options = {
            "bucket_name": bucket_name,
            "custom_domain": None,
            "querystring_auth": True,
            **kwargs,  # allow overrides
        }

        super().__init__(**options)
