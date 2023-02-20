from django.db import models
from django.contrib.auth.models import User

from about.models import Spaces

CATEGORIES = [
    ('U', 'Пользователь'),
    ('T', 'Тренер'),
    ('A', 'Администратор'),
]


class CategoryPerson(models.Model):
    category = models.CharField(max_length=1, choices=CATEGORIES, unique=True)


class UserInfo(models.Model):
    middle_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryPerson, on_delete=models.SET_NULL, null=True, blank=True)


class Images(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='user_id')
    space = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='space_id')
    description = models.TextField(max_length=200, null=True, blank=True)
