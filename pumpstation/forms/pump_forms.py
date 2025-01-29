from django import forms
from django.db.models import fields

class googleMapSearchForm(forms.Form):
    place = forms.CharField(widget=forms.TextInput({
        'placeholder':'Find Pump',
        'style':"border: 0.5px solid #464c53!important; height: 1.8rem !important; border-radius: 0.2rem !important;"
        }))