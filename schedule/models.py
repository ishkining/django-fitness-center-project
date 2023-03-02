from django.db import models

from about.models import Spaces
from user.models import UserInfo


class Hours(models.Model):
    hours_time = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.hours_time}'


class Trainings(models.Model):
    DAYS = [
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
        ('Вс', 'Воскресенье'),
    ]
    name = models.CharField(max_length=50)
    seats = models.IntegerField(max_length=4)
    is_it_for_children = models.BooleanField(default=False)

    space = models.ForeignKey(Spaces, on_delete=models.CASCADE)
    trainer = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    hours = models.ForeignKey(Hours, on_delete=models.CASCADE)
    day = models.CharField(max_length=2, choices=DAYS)
