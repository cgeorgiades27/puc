from django.db import models
from django.utils import timezone
from django.conf import settings


class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField(default=0)
    date_entered = models.DateTimeField(default = timezone.now)
    date_completed = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.date_entered = timezone.now()
        self.save()

    def __str__(self):
        return str(self.user) + "'s log for: " + str(self.date_completed.date()) + ' @ ' + str(self.date_completed.time())  
