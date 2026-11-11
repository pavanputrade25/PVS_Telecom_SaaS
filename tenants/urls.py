
from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_register, name='company_register'),

    path(
        'success/',
        views.registration_success,
        name='registration_success'
    ),

    path(
        'users/',
        views.company_user_management,
        name='company_user_management'
    ),
]
