"""Test utility functions."""
from unittest.mock import patch
from django.test import TestCase, override_settings

from smart_storages.utils import create_storage_class
from smart_storages.storages import SmartS3Storage


class CreateStorageClassTestCase(TestCase):
    """Test cases for create_storage_class utility."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'uploads': {
                'bucket_name': 'test-uploads-bucket',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_create_storage_class(self, mock_init):
        """Test creating a custom storage class."""
        mock_init.return_value = None
        
        # Create a custom storage class
        UploadStorage = create_storage_class(
            'uploads',
            location='uploads',
            default_acl='private',
            file_overwrite=False
        )
        
        # Verify the class was created correctly
        self.assertTrue(issubclass(UploadStorage, SmartS3Storage))
        self.assertEqual(UploadStorage.module_name, 'uploads')
        self.assertEqual(UploadStorage.__name__, 'UploadsStorage')
        
        # Instantiate and verify settings
        storage = UploadStorage()
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-uploads-bucket')
        self.assertEqual(call_kwargs['location'], 'uploads')
        self.assertEqual(call_kwargs['default_acl'], 'private')
        self.assertFalse(call_kwargs['file_overwrite'])

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'custom': {
                'bucket_name': 'test-custom-bucket',
                'location': 'base/',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_create_storage_class_override(self, mock_init):
        """Test that instance settings can override defaults."""
        mock_init.return_value = None
        
        # Create a custom storage class with defaults
        CustomStorage = create_storage_class(
            'custom',
            location='default-location',
            default_acl='private',
        )
        
        # Instantiate with overrides
        storage = CustomStorage(location='override-location')
        
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        # Override should take precedence
        self.assertEqual(call_kwargs['location'], 'override-location')
        # Other defaults should still apply
        self.assertEqual(call_kwargs['default_acl'], 'private')
