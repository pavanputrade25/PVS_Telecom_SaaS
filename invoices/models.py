
from django.db import models
from tenants.models import Tenant


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('INR', 'Indian Rupee'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name='invoices'
    )

    invoice_number = models.CharField(
        max_length=100
    )

    vendor_name = models.CharField(
        max_length=200
    )

    invoice_date = models.DateField()

    billing_period_start = models.DateField()

    billing_period_end = models.DateField()

    invoice_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'invoice_number'],
                name='unique_invoice_number_per_tenant'
            )
        ]

    def __str__(self):
        return f'{self.invoice_number} - {self.vendor_name}'
