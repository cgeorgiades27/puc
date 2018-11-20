from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Entry
from django.db.models import Count, Sum, F, IntegerField
from .forms import EntryForm
from django.contrib.auth.models import User

def log_detail(request, pk):
    log = get_object_or_404(Entry, pk=pk)
    return render(request, 'tracker/log_detail.html', {'log': log})

def user_logs(request, user_id):
    user_logs = Entry.objects.filter(user_id=user_id)
    user = User.objects.filter(id=user_id).values('username')
    return render(request, 'tracker/user_logs.html', {'user_logs': user_logs, 'user': user})

def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')
    total_reps = Entry.objects.values('user').annotate(total=Sum(F('reps')*F('sets'))).order_by('-total')
    users = User.objects.all().order_by('id')
    return render(request, 'tracker/workout_log.html', 
    {
        'logs': logs, 
        'total_reps': total_reps, 
        'users': users,
    })

def log_new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.date_entered = timezone.now()
            entry.save()
            return redirect('log_detail', pk=entry.id)
    else:
        form = EntryForm()
    return render(request, 'tracker/log_new.html', {'form': form})
