from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('trainers/', views.trainers_info, name='trainers-info'),
    path('trainers/<int:id_trainer>', views.trainer_info, name='trainer-info'),

    path('verification/<str:uidb64>/<str:token>/', views.verification, name='verification'),
    path('verification-sent', views.verification_sent, name='verification-sent'),
    path('verification-success', views.verification_success, name='verification-success'),
    path('verification-failed', views.verification_failed, name='verification-failed'),
]