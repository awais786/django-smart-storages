from setuptools import setup, find_packages

setup(
    name="django-smart-storages",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "django>=4.2",
        "django-storages>=1.14.3",  # ✅ this is the key dependency
        "boto3>=1.28.0",            # optional, but usually required for S3
    ],
)
