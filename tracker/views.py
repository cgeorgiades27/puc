from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta, date
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

def competition(request):
    users = User.objects.all().order_by('-id')
    entry = Entry.objects.all()
    startDate = date(2018, 11, 27)
    setRange = Entry.objects.filter(date_completed__gte=startDate)
    todayRange = Entry.objects.filter(date_completed__gte=date.today())
    daysRemaining = (date(2018, 12, 31) - date.today()).days
    todayTotal = todayRange.values('user__username').annotate(todayTotal = Sum(F('reps') * F('sets'))).order_by('-todayTotal')
    remainingPushUps = setRange.values('user__username').annotate(total = 5000 - (Sum(F('reps') * F('sets')))).order_by('total')
    perDay = setRange.values('user__username').annotate(total = (5000 - (Sum(F('reps') * F('sets')))) / daysRemaining).order_by('total')
    return render(request, 'tracker/competition.html', {
        'remainingPushUps': remainingPushUps,
        'users': users,
        'daysRemaining': daysRemaining,
        'entry': entry,
        'todayTotal': todayTotal,
        'perDay': perDay,
    })

def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')

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