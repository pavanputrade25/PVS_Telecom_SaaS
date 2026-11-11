
from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        'invoice_number',
        'vendor_name',
        'tenant',
        'invoice_date',
        'invoice_amount',
        'currency',
        'status',
        'created_at',
    )

    search_fields = (
        'invoice_number',
        'vendor_name',
        'tenant__company_name',
    )

    list_filter = (
        'status',
        'currency',
        'vendor_name',
        'invoice_date',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )
