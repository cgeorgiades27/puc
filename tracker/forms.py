from django import forms
from .models import Entry, Workouts, Profile, Routine, Exercise
from django.forms import formset_factory

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('date_completed', 'workout_title', 'sets', 'reps', 'weight', 'routName')

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

class NewExercise(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('workout', 'treps', 'tsets', 'tweight')

class NewRoutine(forms.ModelForm):
    #exercise_list = forms.ModelMultipleChoiceField(queryset=Exercise.objects.all())
    class Meta:
        model = Routine
        fields = ('name', 'exercise')

    def __init__(self, user, *args, **kwargs):
        super(NewRoutine, self).__init__(*args, **kwargs)
        self.fields['exercise'] = forms.ModelMultipleChoiceField(queryset=Exercise.objects.filter(creator=user).order_by('workout'), widget=forms.CheckboxSelectMultiple())