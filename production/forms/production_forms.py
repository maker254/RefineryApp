from django import forms
from django.db.models import fields

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date = forms.DateField(
            widget=DateInput()
        )