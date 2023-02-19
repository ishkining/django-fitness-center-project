from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),

    path('verification/<str:uidb64>/<str:token>/', views.verification, name='verification'),
    path('verification-sent', views.verification_sent, name='verification-sent'),
    path('verification-success', views.verification_success, name='verification-success'),
    path('verification-failed', views.verification_failed, name='verification-failed'),
]