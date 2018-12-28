from django import forms
from .models import Entry
from .models import UserProfile

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('user', 'date_completed', 'sets', 'reps',)

class ProfileSettings(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'pic_url',)