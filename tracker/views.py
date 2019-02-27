from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from datetime import date, timedelta
from .models import Entry, Workouts, Competition, CompEntry, Profile, CompMember
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Sum, F, IntegerField, Min, Q
from .forms import EntryForm, ProfileForm, NewWorkout, JoinComp


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
                      'user_id': user_id,
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

    # prof = User.objects.annotate(tot=Sum(F('entry__reps') * F('entry__sets')))
    def DateRange(n):
        refDate = date.today() - timedelta(days=n)
        dateSet = Entry.objects.filter(date_completed__gte=refDate)
        return dateSet.values('user__username').annotate(total=Sum(F('reps') * F('sets'))).order_by('-total')

    group10k = DateRange(10000)

    return render(request, 'tracker/workout_log.html',
                  {
                      'group10k': group10k,
                      'logs': logs,
                      # 'prof': prof,
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
                return redirect('log_new')
            else:
                return redirect('login')
    else:
        form = EntryForm()
    return render(request, 'tracker/log_new.html', {'form': form})


def new_workout(request):
    exerciseList = Workouts.objects.all().order_by('workout_title')
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
    return render(request, 'tracker/new_workout.html', {'form': form, 'exerciseList': exerciseList})


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
    members = CompMember.objects.filter(compName_id=compName_id).values('user')
    memberNames = CompMember.objects.filter(compName_id=compName_id).values('user__username') 

    progSet = Entry.objects.filter(
        date_completed__gte=startDate,
        date_completed__lt=endDate,
        workout_title_id__in=workoutID,
        user_id__in=members,
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
        'members': members,
        'memberNames': memberNames,
        'compName_id': compName_id,
    }
                  )


def profile(request):

    #user = request.user
    #comps = CompEntry.objects.filter(user=user).order_by('endDate')    

    if request.user.is_authenticated:
        profile = request.user.profile
        u = profile.user
        qs = Profile.objects.filter(user=u)
        if qs.exists():
            compEntries = CompEntry.objects.all()
            comp = Competition.objects.all()

            progSet = Entry.objects.all().filter(user_id=u.pk)
            progSetSum = progSet.values('workout_title__workout_title').annotate(
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


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            rawPassword = form.cleaned_data.get('password')
            user = authenticate(username=username, password=rawPassword)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


def join_comp(request, compName_id):
    if request.method == 'POST':
        form = JoinComp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comp_entry', compName_id=compName_id)
        else:
            return redirect('competition_list')
    else:
        form = JoinComp()
    return render(request, 'tracker/join_comp.html', {'form': form})
