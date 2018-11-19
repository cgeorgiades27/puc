from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Entry
from django.db.models import Count, Sum, F, IntegerField
from .forms import EntryForm

def log_detail(request, pk):
    log = get_object_or_404(Entry, pk=pk)
    return render(request, 'tracker/log_detail.html', {'log': log})

def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')
    total_reps = Entry.objects.values('user').annotate(total=Sum(F('reps')*F('sets'))).order_by('-total')
    date = timezone.now().date()
    return render(request, 'tracker/workout_log.html', {'logs': logs, 'total_reps': total_reps, 'date': date})

def log_new(request):
    form = EntryForm()
    return render(request, 'tracker/log_edit.html', {'form': form})
