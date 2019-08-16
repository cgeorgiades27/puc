from django import forms
from .models import Entry, Workouts
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder':'Password'}))
        