from django.contrib import admin
from .models import Entry
from .models import UserProfile

admin.site.register(Entry)
admin.site.register(UserProfile)
