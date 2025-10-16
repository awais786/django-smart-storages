"""Test storage backends."""
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings

from smart_storages.storages import (
    SmartS3Storage,
    MediaStorage,
    StaticStorage,
    DocumentStorage,
    PrivateStorage,
    PublicStorage,
)


class SmartS3StorageTestCase(TestCase):
    """Test cases for SmartS3Storage."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'media': {
                'bucket_name': 'test-media-bucket',
                'location': 'media/',
                'default_acl': 'public-read',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_smart_storage_uses_module_config(self, mock_init):
        """Test that SmartS3Storage uses module-specific configuration."""
        mock_init.return_value = None
        
        class TestStorage(SmartS3Storage):
            module_name = 'media'
        
        storage = TestStorage()
        
        # Verify that __init__ was called with the right arguments
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-media-bucket')
        self.assertEqual(call_kwargs['location'], 'media/')
        self.assertEqual(call_kwargs['default_acl'], 'public-read')

    @override_settings(
        AWS_STORAGE_BUCKET_NAME='default-bucket',
        AWS_LOCATION='default/',
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_smart_storage_fallback_to_default(self, mock_init):
        """Test that SmartS3Storage falls back to default settings."""
        mock_init.return_value = None
        
        class TestStorage(SmartS3Storage):
            module_name = 'unconfigured'
        
        storage = TestStorage()
        
        # Verify that __init__ was called with default settings
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'default-bucket')
        self.assertEqual(call_kwargs['location'], 'default/')


class MediaStorageTestCase(TestCase):
    """Test cases for MediaStorage."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'media': {
                'bucket_name': 'test-media-bucket',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_media_storage_initialization(self, mock_init):
        """Test MediaStorage initialization."""
        mock_init.return_value = None
        
        storage = MediaStorage()
        
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-media-bucket')
        self.assertEqual(call_kwargs['location'], 'media')
        self.assertFalse(call_kwargs['file_overwrite'])


class StaticStorageTestCase(TestCase):
    """Test cases for StaticStorage."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'static': {
                'bucket_name': 'test-static-bucket',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_static_storage_initialization(self, mock_init):
        """Test StaticStorage initialization."""
        mock_init.return_value = None
        
        storage = StaticStorage()
        
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-static-bucket')
        self.assertEqual(call_kwargs['location'], 'static')


class DocumentStorageTestCase(TestCase):
    """Test cases for DocumentStorage."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'documents': {
                'bucket_name': 'test-documents-bucket',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_document_storage_initialization(self, mock_init):
        """Test DocumentStorage initialization."""
        mock_init.return_value = None
        
        storage = DocumentStorage()
        
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-documents-bucket')
        self.assertEqual(call_kwargs['location'], 'documents')
        self.assertEqual(call_kwargs['default_acl'], 'private')
        self.assertFalse(call_kwargs['file_overwrite'])


class PrivateStorageTestCase(TestCase):
    """Test cases for PrivateStorage."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'private': {
                'bucket_name': 'test-private-bucket',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_private_storage_initialization(self, mock_init):
        """Test PrivateStorage initialization."""
        mock_init.return_value = None
        
        storage = PrivateStorage()
        
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-private-bucket')
        self.assertEqual(call_kwargs['location'], 'private')
        self.assertEqual(call_kwargs['default_acl'], 'private')
        self.assertFalse(call_kwargs['file_overwrite'])


class PublicStorageTestCase(TestCase):
    """Test cases for PublicStorage."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'public': {
                'bucket_name': 'test-public-bucket',
            },
        }
    )
    @patch('smart_storages.storages.S3Boto3Storage.__init__')
    def test_public_storage_initialization(self, mock_init):
        """Test PublicStorage initialization."""
        mock_init.return_value = None
        
        storage = PublicStorage()
        
        mock_init.assert_called_once()
        call_kwargs = mock_init.call_args[1]
        self.assertEqual(call_kwargs['bucket_name'], 'test-public-bucket')
        self.assertEqual(call_kwargs['location'], 'public')
        self.assertEqual(call_kwargs['default_acl'], 'public-read')
