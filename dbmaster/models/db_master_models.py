from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name =  models.CharField(max_length=50, unique=True)
    #add foreighn key relationship to EAS specs model
    def __str__(self):
        return self.name  

class WeightCategory(models.Model):
    category = models.CharField(max_length=5, blank=False, null=False, default='',unique=True)
    def __str__(self):
        return str(self.category)
    
""" specifies location within plant and conveyor no"""
class Location(models.Model):
    location_name = models.CharField(max_length=10, blank=False, null=False)
    conveyor_code = models.IntegerField(blank=False, null=False)
    def __str__(self):
        return str(self.location_name) + " " + str(self.conveyor_code)

class Device(models.Model):
    ip = models.CharField(max_length=15, blank=False,null=False)
    port = models.IntegerField(blank=False)
    location = models.OneToOneField("Location", on_delete=models.PROTECT, null=True)
    def __str__(self):
        return str(self.pk)
    
"""ADD Ticket Model that sources data from Weighbridge tickets API that has_order and not loaded """
class Ticket(models.Model):
    vehicle_no = models.CharField('Vehicle Number', max_length = 100)
    trailer_no = models.CharField('Trailer Number', max_length = 100, blank=True, null=True)
    bp_name = models.CharField('Business Partner Name', max_length = 100)
    created = models.DateTimeField(auto_now_add = True, editable = False)
    modified = models.DateTimeField(auto_now = True, editable = False)

    has_order = models.BooleanField('Order', default = False)
    has_order_time = models.DateTimeField(null=True, blank=True)
    loaded = models.BooleanField('Loaded', default = False)
    loaded_time = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.vehicle_no)