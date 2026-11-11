
from django.db import models
from django.conf import settings


class Tenant(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.CharField(
        max_length=50,
        unique=True
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name




class TenantMembership(models.Model):

    ROLE_CHOICES = [
        ('company_admin', 'Company Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_memberships'
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='employee'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'user'],
                name='unique_user_per_tenant'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.tenant.company_name} - {self.role}'
