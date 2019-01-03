from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta, date
from .models import Entry
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, IntegerField, Min
from .forms import EntryForm #,ProfileSettings

def log_detail(request, pk):
    log = get_object_or_404(Entry, pk=pk)
    return render(request, 'tracker/log_detail.html', {'log': log})

def user_logs(request, user_id):
    user_logs = Entry.objects.filter(user_id=user_id)
    user = user_logs.values('user__username').first()
    return render(request, 'tracker/user_logs.html', {'user_logs': user_logs, 'user': user})

def workout_by_type(request, user_id, workout_title):
    type_logs = Entry.objects.filter(user_id=user_id, workout_title=workout_title)
    return render(request, 'tracker/type_logs.html', { 'type_logs' : type_logs})

def competition(request):
    entry = Entry.objects.all()
    startDate = date(2018, 11, 27)
    endDate = date(2018, 12, 31)
    setRange = Entry.objects.filter(date_completed__gte=startDate, date_completed__lte=endDate)
    totalPushUps = setRange.values('user__username').annotate(total = (Sum(F('reps') * F('sets')))).order_by('total')
    leader = totalPushUps.first()
    return render(request, 'tracker/competition.html', {
        'totalPushUps' : totalPushUps,
        'entry' : entry,
        'leader' : leader,
    })

def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')
    prof = User.objects.annotate(tot=Sum(F('entry__reps') * F('entry__sets')))
    def DateRange(n):
        refDate = date.today() - timedelta(days = n)
        dateSet = Entry.objects.filter(date_completed__gte = refDate)
        return dateSet.values('user__username').annotate(total = Sum(F('reps') * F('sets'))).order_by('-total')
    group0 = DateRange(0)
    group7 = DateRange(7)
    group30 = DateRange(30)
    group10k = DateRange(10000)

    return render(request, 'tracker/workout_log.html',
                  {
                      'group1': group0,
                      'group7': group7,
                      'group30': group30,
                      'group10k': group10k,
                      'logs': logs,
                      'prof': prof,
                  }
                  )

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
"""
def user_settings(request):
    if request.method == "POST":
        form = ProfileSettings(request.POST)
        if form.is_valid():
            form.pic_url.save()
            return redirect('competition')
    else:
        form = ProfileSettings()
    return render(request, 'tracker/url_new.html', {'form': form})
"""