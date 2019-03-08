from django import forms
from .models import Entry
import django_filters


class EntryFilter(django_filters.FilterSet):
    date_completed = django_filters.NumberFilter(field_name='date_completed' )