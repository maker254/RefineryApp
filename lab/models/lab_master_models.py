from django.db import models
from django.utils import timezone
from django.urls import reverse
from simple_history.models import HistoricalRecords
from dbmaster.models import Brand

class Sample(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class EAS(models.Model):
    name = models.CharField(max_length=12)
    moisture = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    chloride = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    calcium = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    magnesium = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    sulphates = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    alkalinity = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    insoluble_matter = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    iodine_min = models.DecimalField(max_digits=6,decimal_places=2,blank=False, null=True)
    iodine_max = models.DecimalField(max_digits=6,decimal_places=2,blank=False, null=True)
    sieve_size = models.CharField(max_length=6, blank=False)

    def __str__(self):
        return self.name

class COA(models.Model):
    sample = models.ForeignKey('Sample', on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    sampling_date = models.DateField(auto_now_add=False)
    analysis_date = models.DateField(auto_now_add=False)
    batch_no = models.CharField(max_length=7, blank=False)
    moisture = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    chloride = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    calcium = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    magnesium = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    sulphates = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    alkalinity = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    insoluble_matter = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    iodine = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    sieve_size = models.CharField(max_length=6, blank=False)
    eas = models.ForeignKey('EAS', on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    modified_by = models.CharField(max_length=30, blank=True, null=True)  
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['batch_no','brand','sampling_date'], name='unique_brand_batch')
               ]

    def get_absolute_url(self):
        return reverse('lab:coa-details', kwargs={'pk':self.pk})


    
