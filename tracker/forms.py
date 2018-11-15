from djando import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('user', 'date_completed','sets','reps',)