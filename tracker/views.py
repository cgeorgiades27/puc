from django.shortcuts import render
from django.utils import timezone
from .models import Entry

def workout_log(request):
    logs = Entry.objects.all().order_by('date_completed')
    return render(request, 'tracker/workout_log.html', {'logs': logs})
