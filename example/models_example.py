"""
Example Django models showing how to use django-smart-storages.

This example demonstrates:
- Using different storage backends for different fields
- Creating custom storage backends
- Using storage in FileField and ImageField
"""

from django.db import models
from smart_storages.storages import (
    MediaStorage,
    DocumentStorage,
    PrivateStorage,
    PublicStorage,
)
from smart_storages.utils import create_storage_class


# Example 1: Using predefined storage backends
class Article(models.Model):
    """Article model with different storage for different file types."""
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Public image using MediaStorage
    featured_image = models.ImageField(
        upload_to='articles/images/',
        storage=MediaStorage(),
        blank=True,
        null=True,
    )
    
    # Private document using DocumentStorage
    source_document = models.FileField(
        upload_to='articles/sources/',
        storage=DocumentStorage(),
        blank=True,
        null=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Example 2: Creating a custom storage for a specific purpose
ReportStorage = create_storage_class(
    'reports',
    location='reports',
    default_acl='private',
    file_overwrite=False
)


class Report(models.Model):
    """Report model with custom storage."""
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Report file using custom storage
    file = models.FileField(
        upload_to='monthly/',
        storage=ReportStorage(),
    )
    
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Example 3: User-uploaded content with different security levels
class UserProfile(models.Model):
    """User profile with both public and private files."""
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    
    # Public avatar
    avatar = models.ImageField(
        upload_to='avatars/',
        storage=PublicStorage(),
        blank=True,
        null=True,
    )
    
    # Private identity document
    id_document = models.FileField(
        upload_to='documents/identity/',
        storage=PrivateStorage(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Profile for {self.user.username}"


# Example 4: Multi-tenant storage
# Create storage class for each tenant dynamically
def get_tenant_storage(tenant_id):
    """Get storage for a specific tenant."""
    return create_storage_class(
        f'tenant_{tenant_id}',
        location=f'tenants/{tenant_id}/',
        default_acl='private',
    )


class TenantDocument(models.Model):
    """Document model for multi-tenant application."""
    
    tenant_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # File will be stored in tenant-specific bucket
    file = models.FileField(upload_to='documents/')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Override save to use tenant-specific storage."""
        if not self.file.storage:
            TenantStorageClass = get_tenant_storage(self.tenant_id)
            self.file.storage = TenantStorageClass()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Tenant: {self.tenant_id})"


# Example 5: Version-controlled documents
VersionStorage = create_storage_class(
    'versions',
    location='versions',
    default_acl='private',
    file_overwrite=False,  # Never overwrite, keep all versions
)


class DocumentVersion(models.Model):
    """Document version with dedicated version storage."""
    
    document_name = models.CharField(max_length=200)
    version_number = models.IntegerField()
    
    file = models.FileField(
        upload_to='%Y/%m/',  # Organize by date
        storage=VersionStorage(),
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('document_name', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.document_name} v{self.version_number}"
