"""Test configuration utilities."""
from django.test import TestCase, override_settings

from smart_storages.config import get_bucket_config, get_default_bucket_config


class ConfigTestCase(TestCase):
    """Test cases for configuration utilities."""

    @override_settings(
        SMART_STORAGE_BUCKETS={
            'media': {
                'bucket_name': 'test-media-bucket',
                'location': 'media/',
                'default_acl': 'public-read',
            },
            'documents': {
                'bucket_name': 'test-documents-bucket',
                'location': 'documents/',
                'default_acl': 'private',
            },
        }
    )
    def test_get_bucket_config_existing_module(self):
        """Test getting config for an existing module."""
        config = get_bucket_config('media')
        self.assertEqual(config['bucket_name'], 'test-media-bucket')
        self.assertEqual(config['location'], 'media/')
        self.assertEqual(config['default_acl'], 'public-read')

    @override_settings(
        AWS_STORAGE_BUCKET_NAME='default-bucket',
        AWS_LOCATION='default/',
        AWS_DEFAULT_ACL='private',
        SMART_STORAGE_BUCKETS={
            'media': {
                'bucket_name': 'test-media-bucket',
            },
        }
    )
    def test_get_bucket_config_nonexistent_module(self):
        """Test getting config for a non-existent module (should fall back to defaults)."""
        config = get_bucket_config('nonexistent')
        self.assertEqual(config['bucket_name'], 'default-bucket')
        self.assertEqual(config['location'], 'default/')
        self.assertEqual(config['default_acl'], 'private')

    @override_settings(
        AWS_STORAGE_BUCKET_NAME='default-bucket',
        AWS_LOCATION='default/',
        AWS_DEFAULT_ACL='private',
    )
    def test_get_default_bucket_config(self):
        """Test getting default bucket configuration."""
        config = get_default_bucket_config()
        self.assertEqual(config['bucket_name'], 'default-bucket')
        self.assertEqual(config['location'], 'default/')
        self.assertEqual(config['default_acl'], 'private')

    def test_get_bucket_config_empty_settings(self):
        """Test getting config when SMART_STORAGE_BUCKETS is not defined."""
        config = get_bucket_config('media')
        # Should fall back to AWS settings (which may be None)
        self.assertIn('bucket_name', config)
        self.assertIn('location', config)
        self.assertIn('default_acl', config)
