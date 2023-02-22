from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from about.models import Spaces

CATEGORIES = [
    ('U', 'Пользователь'),
    ('T', 'Тренер'),
    ('A', 'Администратор'),
]


class CategoryPerson(models.Model):
    category = models.CharField(max_length=1, choices=CATEGORIES, unique=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{dict(CATEGORIES)[self.category]}'


class UserInfo(models.Model):
    middle_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='user_link')
    category = models.ForeignKey(CategoryPerson, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='category_id')

    class Meta:
        verbose_name_plural = 'Информация о пользователях'

    def __str__(self):
        return f'{self.user}'


class Images(models.Model):
    user = models.ForeignKey(UserInfo, null=True, blank=True, on_delete=models.CASCADE,
                             related_name='user_image')
    space = models.ForeignKey(Spaces, null=True, blank=True, on_delete=models.CASCADE,
                              related_name='space_image')
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Изображения'


class Reviews(models.Model):
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='users')
    trainer = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='trainers')

    class Meta:
        unique_together = (('user', 'trainer'),)
        index_together = (('user', 'trainer'),)
