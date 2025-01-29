from django.db.models.query import QuerySet
from django_filters import FilterSet,CharFilter,ModelChoiceFilter,DateFilter
from django.forms.widgets import TextInput,Select
from django_select2.forms import Select2Widget
from lab.models import COA,Sample
from dbmaster.models import Brand

class COAListFilter(FilterSet):
    #sample = ModelChoiceFilter(queryset=Sample.objects.all(),empty_label='Search sample Type/Name')
    brand = ModelChoiceFilter(queryset=Brand.objects.all(),empty_label='Brand', label="", widget=Select(attrs={'style':' border: 0.7px solid #464c53!important; border-radius: 0.15rem !important; height: 1.9rem !important;'})) 
    batch_no = CharFilter(label='',lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Batch No', 'style':' border: 0.7px solid #464c53!important; border-radius: 0.15rem !important; height: 1.9rem !important;',}))
    sampling_date = DateFilter(label='',lookup_expr='icontains', widget=TextInput(attrs={'type': 'date', 'style':' border: 0.7px solid #464c53!important; border-radius: 0.15rem !important; height: 1.9rem !important;',}))
    class Meta:
        model = COA
        fields =('batch_no', 'brand','sampling_date')