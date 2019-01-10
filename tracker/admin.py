from django.contrib import admin
from .models import Entry, Workouts, Competition, CompEntry, Profile

admin.site.register(Entry)
admin.site.register(Workouts)
admin.site.register(Competition)
admin.site.register(CompEntry)
admin.site.register(Profile)
