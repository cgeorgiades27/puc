from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from datetime import date, timedelta
from .models import Entry, Workouts, Competition, CompEntry
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, IntegerField, Min, Q
from .forms import EntryForm #,ProfileSettings

def log_detail(request, pk):
    log = get_object_or_404(Entry, pk=pk)
    return render(request, 'tracker/log_detail.html', {'log': log})

def user_logs(request, user_id):
    userLogs = Entry.objects.filter(user_id=user_id).order_by('-date_completed')
    user = userLogs.values('user__username').first()
    todaySet = Entry.objects.filter(user_id=user_id, date_completed__gte=datetime.date.today())
    todayTotal = todaySet.values('workout_title__workout_title').annotate(total = (Sum(F('reps') * F('sets'))))
    allTotal = Entry.objects.filter(user_id=user_id).values('workout_title__workout_title').annotate(total = (Sum(F('reps') * F('sets'))))
    return render(request, 'tracker/user_logs.html',
    {
        'userLogs': userLogs,
        'user': user,
        'todayTotal' : todayTotal,
        'allTotal' : allTotal
    })

def workout_by_type(request, user_id, workout_title):
    type_logs = Entry.objects.filter(user_id=user_id, workout_title=workout_title)
    return render(request, 'tracker/type_logs.html', { 'type_logs' : type_logs})

def competition(request):
    entry = Entry.objects.all()
    startDate = date(2018, 11, 27)
    endDate = date(2019, 1, 1)
    setRange = Entry.objects.filter(date_completed__gte=startDate, date_completed__lt=endDate)
    totalPushUps = setRange.values('user__username').annotate(total = (Sum(F('reps') * F('sets')))).order_by('-total')
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

    group10k = DateRange(10000)

    return render(request, 'tracker/workout_log.html',
                  {
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

def competition_list(request):
    competitions = Competition.objects.all().order_by('-compName')
    return render(request, 'tracker/competition_list.html', { 'competitions' : competitions} )

def comp_entry(request, compName_id):
    compEntries = CompEntry.objects.filter(compName_id=compName_id)
    compName = compEntries.values('compName__compName').first()
    startDate = Competition.objects.filter(id=compName_id).values('startDate')
    endDate = Competition.objects.filter(id=compName_id).values('endDate')
    maxID = list(CompEntry.objects.values('workout_title_id').last().values())
    progSet = Entry.objects.filter(date_completed__gte=startDate, date_completed__lt=endDate, workout_title_id__lte=maxID[0])
    return render(request, 'tracker/comp_entry.html', {
        'compEntries' : compEntries,
        'compName' : compName,
        'startDate' : startDate,
        'endDate' : endDate,
        'progSet' : progSet,
        }
        )
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