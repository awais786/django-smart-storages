MEDIA_URL = "/media/"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

SECRET_KEY = "tests"

USE_TZ = True

AWS_STORAGE_BUCKET_NAME = "test-bucket"
