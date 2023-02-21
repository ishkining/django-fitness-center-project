from django.db import models

TYPE_SPACES = [
    ('L', 'Комната'),
    ('B', 'Комплекс'),
]


class Spaces(models.Model):
    description = models.TextField(max_length=500)
    type = models.CharField(max_length=1, choices=TYPE_SPACES)

    class Meta:
        verbose_name_plural = 'Пространства'
