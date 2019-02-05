from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from datetime import date, timedelta
from .models import Entry, Workouts, Competition, CompEntry, Profile, Routine, Exercise
#from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, IntegerField, Min, Q
from .forms import EntryForm, ProfileForm, NewWorkout, NewRoutine, NewExercise


def log_detail(request, pk):
    log = get_object_or_404(Entry, pk=pk)
    return render(request, 'tracker/log_detail.html', {'log': log})


def user_logs(request, user_id):
    userLogs = Entry.objects.filter(user_id=user_id).order_by('-date_completed')
    userLogs50 = Entry.objects.filter(user_id=user_id).order_by('-date_completed')[:50]
    user = userLogs.values('user__username').first()
    todaySet = Entry.objects.filter(user_id=user_id, date_completed__gte=datetime.date.today())
    todayTotal = todaySet.values('workout_title__workout_title').annotate(total=(Sum(F('reps') * F('sets'))))
    allTotal = Entry.objects.filter(user_id=user_id).values('workout_title__workout_title').annotate(
        total=(Sum(F('reps') * F('sets')))).order_by('-total')
    prof = Profile.objects.get(user_id=user_id)

    return render(request, 'tracker/user_logs.html',
                  {
                      'userLogs': userLogs,
                      'userLogs50': userLogs50,
                      'user': user,
                      'todayTotal': todayTotal,
                      'allTotal': allTotal,
                      'prof': prof,
                  })


def all_user_logs(request, user_id):
    userLogs = Entry.objects.filter(user_id=user_id).order_by('-date_completed')
    user = userLogs.values('user__username').first()

    return render(request, 'tracker/all_user_logs.html', {'userLogs': userLogs, 'user': user})

def workout_by_type(request, user_id, workout_title):
    type_logs = Entry.objects.filter(user_id=user_id, workout_title=workout_title)
    return render(request, 'tracker/type_logs.html', {'type_logs': type_logs})


def competition(request):
    entry = Entry.objects.all()
    startDate = date(2018, 11, 27)
    endDate = date(2019, 1, 1)
    setRange = Entry.objects.filter(date_completed__gte=startDate, date_completed__lt=endDate)
    totalPushUps = setRange.values('user__username').annotate(total=(Sum(F('reps') * F('sets')))).order_by('-total')
    leader = totalPushUps.first()
    return render(request, 'tracker/competition.html', {
        'totalPushUps': totalPushUps,
        'entry': entry,
        'leader': leader,
    })


def all_logs(request):
    logs = Entry.objects.all().order_by('-date_completed', 'user_id')

    return render(request, 'tracker/all_logs.html', {'logs': logs})


def workout_log(request):
    logs = Entry.objects.all().order_by('-date_completed')[:50]

    def DateRange(n):
        refDate = date.today() - timedelta(days=n)
        dateSet = Entry.objects.filter(date_completed__gte=refDate)
        return dateSet.values('user__username').annotate(total=Sum(F('reps') * F('sets'))).order_by('-total')

    group10k = DateRange(10000)

    return render(request, 'tracker/workout_log.html',
                  {
                      'group10k': group10k,
                      'logs': logs,
                  }
                  )


def log_new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                entry = form.save(commit=False)
                entry.date_entered = timezone.now()
                entry.user = request.user
                entry.save()
                return redirect('log_detail', pk=entry.id)
            else:
                return redirect('login')
    else:
        form = EntryForm()
    return render(request, 'tracker/log_new.html', {'form': form})


def new_workout(request):
    if request.method == "POST":
        form = NewWorkout(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return redirect('log_new')
        else:
            return redirect('new_workout')
    else:
        form = NewWorkout()
    return render(request, 'tracker/new_workout.html', {'form': form})


def competition_list(request):
    competitions = Competition.objects.all().order_by('-endDate')
    today = date.today()
    return render(request, 'tracker/competition_list.html', {'competitions': competitions, 'today': today})


def comp_entry(request, compName_id):
    compEntries = CompEntry.objects.filter(compName_id=compName_id).order_by('workout_title__workout_title')
    compName = compEntries.values('compName__compName').first()
    sDate = Competition.objects.filter(id=compName_id)
    startDate = Competition.objects.filter(id=compName_id).values('startDate')
    endDate = Competition.objects.filter(id=compName_id).values('endDate')
    workoutID = CompEntry.objects.filter(compName_id=compName_id).values('workout_title_id')

    progSet = Entry.objects.filter(
        date_completed__gte=startDate,
        date_completed__lt=endDate,
        workout_title_id__in=workoutID
    )

    progSetSum = progSet.values('user__username', 'workout_title__workout_title').annotate(
        total=Sum(F('sets') * F('reps'))).order_by('-total', 'user__username')

    return render(request, 'tracker/comp_entry.html', {
        'compEntries': compEntries,
        'compName': compName,
        'startDate': startDate,
        'endDate': endDate,
        'progSetSum': progSetSum,
        'sDate': sDate,
    }
                  )


def profile(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        u = profile.user
        qs = Profile.objects.filter(user=u)
        if qs.exists():
            compEntries = CompEntry.objects.all()
            comp = Competition.objects.all()

            progSet = Entry.objects.all()
            progSetSum = progSet.values('user__username', 'workout_title__workout_title').annotate(
                total=Sum(F('sets') * F('reps')))

            return render(request, 'tracker/profile.html', {
                'profile': profile,
                'compEntries': compEntries,
                'comp': comp,
                'progSetSum': progSetSum,
            }
                          )
        else:
            return redirect('update_profile')
    else:
        return redirect('login')


def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'tracker/update_profile.html', {
        'profile_form': profile_form
    })

def new_exercise(request):
    if request.user.is_authenticated:
        u = request.user
        myexer = Exercise.objects.filter(creator=u).order_by('workout')
        if request.method == "POST":
            form = NewExercise(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.creator = request.user
                entry.save()
                return redirect('new_exercise')
            else:
                return redirect('new_exercise')
        else:
            form = NewExercise()
            return render(request, 'tracker/new_exercise.html', {
                'form': form,
                'myexer': myexer,
                })
    else:
        return redirect('login')

def exercise_next(request):
    if request.method == "POST":
        form = NewExercise(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.creator = request.user
            entry.save()
            return redirect('new_routine')
        else:
            return redirect('new_exercise')
    else:
        form = NewExercise()
        return render(request, 'tracker/new_exercise.html', {'form': form})

def new_routine(request):
    if request.user.is_authenticated:
        u = request.user
        if request.method == "POST":
            form = NewRoutine(request.user, request.POST)
            if form.is_valid():
                    entry = form.save(commit=False)
                    entry.creator = u
                    entry.save()
                    form.save_m2m()
                    return redirect('routine_detail', rout=entry.id)
            else:
                return redirect('new_exercise')

        else:
            form = NewRoutine(request.user)
            return render(request, 'tracker/new_routine.html', {'form': form})
    else:
        return redirect('login')

def routine_detail(request, rout):
    log = get_object_or_404(Routine, id=rout)
    return render(request, 'tracker/routine_detail.html', {'log': log})