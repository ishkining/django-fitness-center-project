from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_schedule, name='show-schedule'),
]