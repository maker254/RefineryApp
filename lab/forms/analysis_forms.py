from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import Select, Widget
from django_select2.forms import Select2Widget
from django.forms import modelformset_factory
from lab.models import Sample,COA
from dbmaster.models import Brand

class DateInput(forms.DateInput):
    input_type = 'date'

class COAForm(forms.ModelForm):
    class Meta:
        model = COA
        fields =  ['sample', 'brand', 'sampling_date','batch_no', 'moisture',
                    'chloride', 'calcium', 'magnesium', 'sulphates', 'alkalinity', 'insoluble_matter', 'iodine','sieve_size'
                ]
       
    sample = forms.ModelChoiceField(
        queryset = Sample.objects.all(),
        )
    brand = forms.ModelChoiceField(
        queryset = Brand.objects.all(),
        required=True,
        )
    sampling_date = forms.DateField(
        widget=DateInput(),
        required=True,
        )
    moisture = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True, 
        )
    chloride = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True, 
        )
        
    calcium = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True, 
        )
    magnesium = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True, 
        )
    sulphates = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True, 
        )
    alkalinity = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True,
        )
    insoluble_matter = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True, 
        )
    iodine = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class':'text-center',
            }),
        required=True,
        )
    sieve_size = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'text-center',
            }) 
        )

class COAPrintForm(forms.Form):
    batchno = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                'id':'batch-search',
                'placeholder': 'search',
                'style': 'text-align:center ; background-color:white;'}
        )
    )

BaseCOAFormset = modelformset_factory(COA, form=COAForm, extra=10,can_delete=False)

#create formset from base formset with no initial instances of model
class COAFormset(BaseCOAFormset): 
    def __init__(self, *args, **kwargs):
        super(BaseCOAFormset, self).__init__(*args, **kwargs)
        self.queryset = COA.objects.none()
