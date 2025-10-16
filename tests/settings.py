"""Django settings for running tests."""
import os

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'test-secret-key-for-testing-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'smart_storages',
]

MIDDLEWARE = []

ROOT_URLCONF = ''

TEMPLATES = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AWS Settings for testing
AWS_ACCESS_KEY_ID = 'test-access-key'
AWS_SECRET_ACCESS_KEY = 'test-secret-key'
AWS_STORAGE_BUCKET_NAME = 'test-default-bucket'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_LOCATION = ''
AWS_DEFAULT_ACL = None

# Smart storage buckets configuration
SMART_STORAGE_BUCKETS = {
    'media': {
        'bucket_name': 'test-media-bucket',
        'location': 'media/',
        'default_acl': 'public-read',
    },
    'static': {
        'bucket_name': 'test-static-bucket',
        'location': 'static/',
        'default_acl': 'public-read',
    },
    'documents': {
        'bucket_name': 'test-documents-bucket',
        'location': 'documents/',
        'default_acl': 'private',
    },
}
