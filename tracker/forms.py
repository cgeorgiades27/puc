from django import forms
from .models import Entry, Workouts, CompMember
from .models import Profile

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('date_completed', 'workout_title', 'sets', 'reps', 'weight')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'pic_url', 'bday', 'motto')

"""
class ProfileSettings(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'pic_url',)
"""

class NewWorkout(forms.ModelForm):
    class Meta:
        model = Workouts
        fields = ('workout_title', 'workout_url')


class JoinComp(forms.ModelForm):
    class Meta:
        model = CompMember
        fields = ('compName', 'user')
