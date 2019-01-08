from django.contrib import admin
from .models import Entry, Workouts, Competition, CompEntry
#from .models import UserProfile

admin.site.register(Entry)
admin.site.register(Workouts)
admin.site.register(Competition)
admin.site.register(CompEntry)
#admin.site.register(UserProfile)
