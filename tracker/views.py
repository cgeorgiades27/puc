from django.shortcuts import render
from django.utils import timezone
from .models import Entry
from django.db.models import Count, Sum, F, IntegerField

def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')
    reps = Entry.objects.all().aggregate(total = Sum(F('reps')*F('sets'), output_field=IntegerField()))
    date = timezone.now().date()
    return render(request, 'tracker/workout_log.html', {'logs': logs, 'reps': reps, 'date': date})
