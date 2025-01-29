from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import Select, Widget
from django_select2.forms import ModelSelect2Widget, Select2Widget
from sales.models import Counter
from dbmaster.models import Device,Ticket

def getUsedDevices():
    activeCounters = Counter.objects.distinct()
    usedDevices =[ item.device.ip for item in activeCounters]
    return usedDevices

def getActiveCounterTickets():
    activeCounters = Counter.objects.distinct()
    servicedTickets = [ item.ticket.vehicle_no for item in activeCounters]
    return servicedTickets

def getActiveCounters():
    activeCounters = [item.device.ip for item in Counter.objects.distinct().filter(closed=False)]
    return activeCounters

class SetCounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = "__all__"

    device =forms.ModelChoiceField( queryset=Device.objects.all(), 
            label="Gate No",
            empty_label="Select Gate",
            widget=Select2Widget(attrs={
                 'class': 'form-control',
                 'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 100px !important;',
                }),
            )
    ticket = forms.ModelChoiceField( queryset=Ticket.objects.all(), 
            label="Vehicle No",
            empty_label="Select Vehicle No",
            widget=Select2Widget(attrs={
                 'class': 'form-control',
                 'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;' ,
                }),
            )
    order_50 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bags",
            'class': 'form-control',
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_25 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bags",
            'class': 'form-control',
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_20 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bales",
            'class': 'form-control',
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_6  = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bales",
            'class': 'form-control',
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    
    def __init__(self,*args, **kwargs):
        super(SetCounterForm, self).__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.all().exclude(ip__in=getActiveCounters())
        self.fields['ticket'].queryset = Ticket.objects.all().filter(loaded=False).exclude(vehicle_no__in=getActiveCounterTickets())

class CounterCreateForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = "__all__"

    device =forms.ModelChoiceField( queryset=Device.objects.all(), 
            label="Gate No",
            empty_label="Select Loading Gate",
            widget=Select2Widget(attrs={
                 'class': 'form-control',
                 'style':'min-width: 120px !important; background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important;',}),
            )
    ticket = forms.ModelChoiceField( queryset=Ticket.objects.all(), 
            label="Vehicle No",
            empty_label="Select Vehicle No",
            widget=Select2Widget(attrs={
                 'class': 'form-control',
                 'style':'min-width: 120px !important; background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important;',}),
            )
    order_50 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bags",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_25 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bags",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_20 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bales",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_6  = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bales",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    
    def __init__(self,*args, **kwargs):
        super(CounterCreateForm, self).__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.all().exclude(ip__in=getUsedDevices())
        self.fields['ticket'].queryset = Ticket.objects.all().exclude(vehicle_no__in=getActiveCounterTickets())
    

"""Find a workaround for this i.e use same form for create and update views"""
class CounterUpdateForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = "__all__"

    device =forms.ModelChoiceField( queryset=Device.objects.all(),
            label="Gate No",
            empty_label="Select Loading Gate",
            widget=Select2Widget(attrs={
                 'class': 'form-control',
                 'style':'min-width: 120px !important; background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important;',}),
            )
    ticket = forms.ModelChoiceField( queryset=Ticket.objects.all(),
            label="Vehicle No",
            empty_label="Select Vehicle No",
            widget=Select2Widget(attrs={
                 'class': 'form-control',
                 'style':'min-width: 120px !important; background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important;',}),
            )
    order_50 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bags",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_25 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bags",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_20 = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bales",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))
    order_6  = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': "No. of bales",
            'style':'background-color: white !important; border:1px solid #dee2e6 !important; border-radius:5px !important; min-width: 50px !important;'
        }))


