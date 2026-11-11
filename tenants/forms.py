
from django import forms
from .models import Tenant


class TenantRegistrationForm(forms.ModelForm):

    class Meta:
        model = Tenant

        fields = [
            'company_name',
            'company_code',
            'email',
            'phone',
            'address',
        ]

        widgets = {
            'company_name': forms.TextInput(
                attrs={'placeholder': 'Enter company name'}
            ),
            'company_code': forms.TextInput(
                attrs={'placeholder': 'Example: ABC001'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter business email'}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Enter phone number'}
            ),
            'address': forms.Textarea(
                attrs={
                    'placeholder': 'Enter company address',
                    'rows': 3
                }
            ),
        }

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class CompanyUserCreationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter password'}
        ),
        validators=[validate_password]
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm password'}
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Enter username'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter business email'}
            ),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last name'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error(
                'confirm_password',
                'Passwords do not match.'
            )

        if password:
            try:
                password_validation.validate_password(
                    password,
                    self.instance
                )
            except ValidationError as error:
                self.add_error('password', error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
