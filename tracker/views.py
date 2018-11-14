from django.shortcuts import render

def workout_log(request):
    return render(request, 'tracker/workout_log.html', {})
