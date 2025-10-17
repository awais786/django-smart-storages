# tests/test_storages.py
import os
from django.test import TestCase
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from smart_storages.s3_backend import BaseSpecialS3Storage

# Ensure Django settings are configured for standalone test runs
if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_storages.tests.settings")


class ImportExportS3Storage(BaseSpecialS3Storage):
    storage_key = "import_export"


class AnalyticsS3Storage(BaseSpecialS3Storage):
    storage_key = "analytics"


class DefaultsS3Storage(AnalyticsS3Storage):
    storage_key = "none"


class TestSpecialStorages(TestCase):
    def test_base_storage_uses_default_bucket(self):
        """Fallback to AWS_STORAGE_BUCKET_NAME if specific bucket setting is missing."""
        storage = DefaultsS3Storage()
        self.assertIsInstance(storage, S3Boto3Storage)
        self.assertEqual(storage.bucket_name, settings.AWS_STORAGE_BUCKET_NAME)
        self.assertFalse(storage.querystring_auth)
        self.assertEqual(storage.default_acl, "private")
        self.assertEqual(storage.object_parameters, {"CacheControl": "max-age=3600"})

    def test_custom_bucket_is_used(self):
        """The class should pick up its bucket name from the STORAGES dict."""
        storage = ImportExportS3Storage()
        self.assertEqual(storage.bucket_name, "import_export")

    def test_multiple_subclasses_can_have_different_buckets(self):
        """Each subclass can have its own bucket."""
        export_storage = ImportExportS3Storage()
        analytics_storage = AnalyticsS3Storage()
        self.assertNotEqual(export_storage.bucket_name, analytics_storage.bucket_name)
        self.assertEqual(export_storage.bucket_name, settings.STORAGES["import_export"]["OPTIONS"]["bucket_name"])
        self.assertEqual(analytics_storage.bucket_name, settings.STORAGES["analytics"]["OPTIONS"]["bucket_name"])

    def test_init_allows_overriding_default_kwargs(self):
        """User-provided kwargs override defaults."""
        storage = ImportExportS3Storage(querystring_auth=False)
        self.assertFalse(storage.querystring_auth)
        self.assertEqual(storage.bucket_name, settings.STORAGES["import_export"]["OPTIONS"]["bucket_name"])

    def test_acl_can_be_customized(self):
        """Custom ACLs are respected."""
        storage = ImportExportS3Storage(default_acl="public-read")
        self.assertEqual(storage.default_acl, "public-read")

    def test_combined_overrides_with_acl(self):
        """ACL and querystring_auth can both be customized."""
        storage = ImportExportS3Storage(default_acl="private", querystring_auth=False)
        self.assertEqual(storage.default_acl, "private")
        self.assertFalse(storage.querystring_auth)
