
from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice

        fields = [
            'invoice_number',
            'vendor_name',
            'invoice_date',
            'billing_period_start',
            'billing_period_end',
            'invoice_amount',
            'currency',
            'description',
        ]

        widgets = {
            'invoice_number': forms.TextInput(attrs={
                'placeholder': 'Enter invoice number'
            }),

            'vendor_name': forms.TextInput(attrs={
                'placeholder': 'Enter telecom vendor name'
            }),

            'invoice_date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'billing_period_start': forms.DateInput(attrs={
                'type': 'date'
            }),

            'billing_period_end': forms.DateInput(attrs={
                'type': 'date'
            }),

            'invoice_amount': forms.NumberInput(attrs={
                'placeholder': 'Enter invoice amount',
                'min': '0',
                'step': '0.01'
            }),

            'currency': forms.Select(),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter invoice description',
                'rows': 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('billing_period_start')
        end_date = cleaned_data.get('billing_period_end')
        amount = cleaned_data.get('invoice_amount')

        if start_date and end_date and start_date > end_date:
            self.add_error(
                'billing_period_end',
                'Billing end date cannot be earlier than start date.'
            )

        if amount is not None and amount < 0:
            self.add_error(
                'invoice_amount',
                'Invoice amount cannot be negative.'
            )

        return cleaned_data
