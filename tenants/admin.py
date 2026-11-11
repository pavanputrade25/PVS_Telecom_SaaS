
from django.contrib import admin
from .models import Tenant, TenantMembership


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'company_code',
        'email',
        'is_active',
        'created_at',
    )

    search_fields = (
        'company_name',
        'company_code',
        'email',
    )

    list_filter = ('is_active',)


@admin.register(TenantMembership)
class TenantMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'tenant',
        'role',
        'is_active',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'tenant__company_name',
    )

    list_filter = (
        'role',
        'is_active',
        'tenant',
    )
