
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .forms import (
    TenantRegistrationForm,
    CompanyUserCreationForm
)
from .models import TenantMembership


def company_register(request):

    if request.method == 'POST':
        form = TenantRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('registration_success')

    else:
        form = TenantRegistrationForm()

    return render(
        request,
        'tenants/company_register.html',
        {'form': form}
    )


def registration_success(request):
    return render(
        request,
        'tenants/registration_success.html'
    )


@login_required
def company_user_management(request):

    membership = TenantMembership.objects.filter(
        user=request.user,
        is_active=True,
        role='company_admin',
        tenant__is_active=True
    ).select_related('tenant').first()

    if membership is None:
        raise PermissionDenied(
            "You do not have permission to manage company users."
        )

    tenant = membership.tenant

    if request.method == 'POST':
        form = CompanyUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            TenantMembership.objects.create(
                tenant=tenant,
                user=user,
                role='employee'
            )

            messages.success(
                request,
                f"User {user.username} created successfully."
            )

            return redirect('company_user_management')

    else:
        form = CompanyUserCreationForm()

    company_users = TenantMembership.objects.filter(
        tenant=tenant
    ).select_related('user').order_by('-created_at')

    return render(
        request,
        'tenants/company_users.html',
        {
            'form': form,
            'company_users': company_users,
            'tenant': tenant
        }
    )
