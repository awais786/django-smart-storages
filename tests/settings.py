MEDIA_URL = "/media/"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

SECRET_KEY = "tests"

USE_TZ = True


AWS_STORAGE_BUCKET_NAME = "default-bucket"

INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "storages", "smart_storages"]

STORAGES = {
    "import_export": {
        "BACKEND": "tests.test_storages.ImportExportS3Storage",
        "OPTIONS": {"custom_domain": None, "querystring_auth": True, "bucket_name": "import_export"},
    },
    "analytics": {
        "BACKEND": "tests.test_storages.AnalyticsS3Storage",
        "OPTIONS": {"custom_domain": None, "bucket_name": "analytics"},
    },
}
