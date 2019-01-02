from django import forms
from .models import Entry, Workouts
#from .models import UserProfile

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('user', 'date_completed', 'workout_title', 'sets', 'reps',)
"""
class ProfileSettings(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'pic_url',)
"""