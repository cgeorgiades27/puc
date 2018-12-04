from django.db import models
from django.utils import timezone
from django.conf import settings

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
    date_entered = models.DateTimeField(default = timezone.now)
    date_completed = models.DateTimeField(blank = True, null = True, default = timezone.now)

    def publish(self):
        self.date_entered = timezone.now()
        self.save()
        
    def total(self):
        total = self.reps * self.sets
        return total
    
    def __str__(self):
        return "Entry: " +  str(self.id) + " - " + str(self.user) + "date: " + str(self.date_completed)
        
