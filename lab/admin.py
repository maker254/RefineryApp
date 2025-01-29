from django.contrib import admin
from lab.models import *

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(EAS)
class EASAdmin(admin.ModelAdmin):
    list_display = ('name','moisture', 'chloride','calcium', 'magnesium', 'sulphates', 'alkalinity', 'insoluble_matter','iodine_min', 'iodine_max', 'sieve_size')

@admin.register(COA)
class COAAdmin(admin.ModelAdmin):
    list_display = ('batch_no','sample', 'brand', 'sampling_date', 'analysis_date', 'moisture', 'chloride',
                    'calcium', 'magnesium', 'sulphates', 'alkalinity', 'insoluble_matter', 'iodine',  'eas', 'modified_by', 'created')
    list_filter = ('sampling_date', 'brand')
