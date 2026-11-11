
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Invoice
from .forms import InvoiceForm
from tenants.models import TenantMembership


def get_user_tenant(user):
    membership = TenantMembership.objects.filter(
        user=user,
        is_active=True,
        tenant__is_active=True
    ).select_related('tenant').first()

    if membership is None:
        raise PermissionDenied(
            "You are not assigned to an active company."
        )

    return membership


@login_required
def invoice_list(request):

    membership = get_user_tenant(request.user)

    invoices = Invoice.objects.filter(
        tenant=membership.tenant
    ).order_by('-created_at')

    return render(
        request,
        'invoices/invoice_list.html',
        {
            'invoices': invoices,
            'tenant': membership.tenant
        }
    )


@login_required
def invoice_create(request):

    membership = get_user_tenant(request.user)

    if membership.role not in ['company_admin', 'manager']:
        raise PermissionDenied(
            "You do not have permission to create invoices."
        )

    if request.method == 'POST':
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice = form.save(commit=False)

            # Automatically assign the logged-in user's company
            invoice.tenant = membership.tenant

            invoice.save()

            messages.success(
                request,
                f"Invoice {invoice.invoice_number} created successfully!"
            )

            return redirect('invoice_list')

    else:
        form = InvoiceForm()

    return render(
        request,
        'invoices/invoice_form.html',
        {
            'form': form,
            'tenant': membership.tenant
        }
    )
