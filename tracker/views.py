from django.shortcuts import render
from django.utils import timezone
from .models import Entry
from django.db.models import Count, Sum, F, IntegerField

def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')
    total_reps = Entry.objects.values('user').annotate(total=Sum(F('reps')*F('sets'))).order_by('-total')
    date = timezone.now().date()
    return render(request, 'tracker/workout_log.html', {'logs': logs, 'total_reps': total_reps, 'date': date})
