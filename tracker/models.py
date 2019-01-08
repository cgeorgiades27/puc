from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

class Workouts(models.Model):
    workout_title = models.CharField(max_length = 50)
    workout_url = models.URLField(max_length = 500, null = True, blank = True)
    
    def __str__(self):
        return self.workout_title

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    pic_url = models.CharField(max_length=300, default="https://i.ytimg.com/vi/TONW3GOKrUY/hqdefault.jpg")
"""

class Competition(models.Model):
    compName = models.CharField(max_length=100)
    startDate = models.DateTimeField(default = timezone.now)
    endDate = models.DateTimeField(blank = True, null = True)
    
    def __str__(self):
        return str(self.compName) + " " + str(self.id)

class CompEntry(models.Model):
    compName = models.ForeignKey(Competition, related_name = 'competition', on_delete=models.CASCADE)
    workout_title = models.ForeignKey(Workouts, on_delete = models.CASCADE)
    totalReps = models.IntegerField()

    def __str__(self):
        return str(self.compName) + " " + "entry: " + str(self.id)

class Entry(models.Model):
    user = models.ForeignKey(User, related_name='entry', on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
    weight = models.IntegerField(blank = True, null = True)
    date_entered = models.DateTimeField(default = timezone.now)
    date_completed = models.DateTimeField(blank = True, null = True, default = timezone.now)
    workout_title = models.ForeignKey(Workouts, related_name='workouts', on_delete=models.CASCADE, null = True)
    compName = models.ForeignKey(Competition, blank = True, null = True, on_delete=models.CASCADE)

    def publish(self):
        self.date_entered = timezone.now()
        self.save()

    def total(self):
        total = self.reps * self.sets
        return total

    def __str__(self):
        return "Entry: " +  str(self.id) + " - " + str(self.user) + "date: " + str(self.date_completed)
