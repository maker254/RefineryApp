from django.db.models import fields
import django_tables2 as tables
from lab.models import COA

class COAListTAble(tables.Table):
    #id = tables.Column(linkify=True)
    sample=tables.Column(verbose_name='Sample Name',attrs={"th":{"style": "font-size:0.95rem;"},"td":{'style': "font-size:0.85rem;",'class':'text-left !important;'}}) 
    brand = tables.Column(verbose_name='Brand Name', linkify=True ,attrs={'target':'_blank',"th": {"id": "brand-column","style": "font-size:0.95rem;","class":"text-left"},
                                                                    "td": {"id": "brand-column",'style': "font-size:0.85rem;",'class':'text-left !important;'}})
    batch_no = tables.Column(verbose_name="Batch No.",linkify=True,attrs={"th":{"style": "font-size:0.95rem;"}, "td":{"class":"text-left","style":"font-size:0.85rem !important;"},})
    sampling_date = tables.Column(verbose_name="Sampling Date")
    chloride = tables.Column(verbose_name="NaCl")

    class Meta:
        model = COA
        template_name = "includes/bootstrap4.html"
        attrs ={
            "class": "table table-sm table-bordered table-striped table-hover text-nowrap",
            "style": {"border": "2px !important;","min-width": "1115px !important"},
            "thead": {"class":"thead-light"},
            "th": {"style": "font-size:0.95rem; color:black !important;"},
            "td":{"class":"text-left", "style": "font-size:0.85rem !important;"},
            "id": "coa-list-table"
            }
        empty_text = "There are no entries matching the search criteria..."
        fields =('sampling_date','batch_no', 'brand','sample', 'chloride','iodine', 'calcium', 'magnesium', 'sulphates', 'alkalinity', 'moisture')


