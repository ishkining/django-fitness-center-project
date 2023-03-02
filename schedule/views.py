from django.shortcuts import render

from .models import Hours


def show_schedule(request):
    hours = Hours.objects.all()
    context = {
        'hours': hours
    }
    return render(request, 'schedule/show-schedule.html', context)
