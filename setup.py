from setuptools import setup, find_packages

setup(
    name="django-smart-storages",
    version="0.1.0",
    packages=find_packages(include=["smart_storages", "smart_storages.*"]),
    install_requires=[
        "django-storages>=1.14.3",  # S3 backend dependency
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
)
