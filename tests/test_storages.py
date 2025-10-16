from django.test import TestCase, override_settings
from storages.backends.s3boto3 import S3Boto3Storage

from smart_storages.s3_backend import BaseSpecialS3Storage


class ImportExportS3Storage(BaseSpecialS3Storage):
    setting_name = "COURSE_IMPORT_EXPORT_BUCKET"


class AnalyticsS3Storage(BaseSpecialS3Storage):
    setting_name = "ANALYTICS_BUCKET"


class TestSpecialStorages(TestCase):
    @override_settings(AWS_STORAGE_BUCKET_NAME="default-bucket")
    def test_base_storage_uses_default_bucket(self):
        """
        If the specific bucket setting is missing, BaseSpecialS3Storage
        should fall back to AWS_STORAGE_BUCKET_NAME.
        """
        storage = ImportExportS3Storage()
        self.assertIsInstance(storage, S3Boto3Storage)
        self.assertEqual(storage.bucket_name, "default-bucket")
        self.assertTrue(storage.querystring_auth)

    @override_settings(COURSE_IMPORT_EXPORT_BUCKET="import-export-bucket")
    def test_custom_bucket_is_used(self):
        """
        The class should pick up its bucket name from the setting defined
        in `setting_name`.
        """
        storage = ImportExportS3Storage()
        self.assertEqual(storage.bucket_name, "import-export-bucket")

    @override_settings(
        ANALYTICS_BUCKET="analytics-bucket",
        AWS_STORAGE_BUCKET_NAME="default-bucket",
    )
    def test_multiple_subclasses_can_have_different_buckets(self):
        """
        Each subclass should independently use its own bucket setting.
        """
        export_storage = ImportExportS3Storage()
        analytics_storage = AnalyticsS3Storage()

        self.assertNotEqual(export_storage.bucket_name, analytics_storage.bucket_name)
        self.assertEqual(export_storage.bucket_name, "default-bucket")  # falls back
        self.assertEqual(analytics_storage.bucket_name, "analytics-bucket")

    @override_settings(COURSE_IMPORT_EXPORT_BUCKET="import-bucket")
    def test_init_allows_overriding_default_kwargs(self):
        """
        Users can override default kwargs such as querystring_auth.
        """
        storage = ImportExportS3Storage(querystring_auth=False)
        self.assertFalse(storage.querystring_auth)
        self.assertEqual(storage.bucket_name, "import-bucket")
