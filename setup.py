"""Setup configuration for django-smart-storages."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-smart-storages",
    version="0.1.0",
    author="Awais Qureshi",
    author_email="awais.qureshi@arbisoft.com",
    description="A Django plugin for using different storage buckets for different modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/awais786/django-smart-storages",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "django-storages>=1.12",
        "boto3>=1.20",
    ],
)
