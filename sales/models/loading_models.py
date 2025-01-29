from django.db import models
from django.utils import timezone
from django.urls import reverse
from dbmaster.models import WeightCategory,Device,Ticket
from simple_history.models import HistoricalRecords
 
     
class Counter(models.Model): #controls servicing of orders to belts/devices and ON/OFF Belt control
    device = models.ForeignKey(Device, on_delete=models.PROTECT) #only one record per device can exist at any given time
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    order_50 = models.IntegerField(blank=False, default=0)
    order_25 = models.IntegerField(blank=False, default=0)
    order_20 = models.IntegerField(blank=False, default=0)
    order_6  = models.IntegerField(blank=False, default=0)
    closed = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return(str(self.device))
    
    def get_absolute_url(self):
        return reverse('sales:counter-update', kwargs={'pk':self.pk})
    
class ServedOrder(models.Model): #contains order details
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    counter_no = models.ForeignKey(Counter, on_delete=models.PROTECT)
    loaded_quantity = models.IntegerField(blank=True)  #quantity ordered
    cnt_50 = models.IntegerField(blank=False, null=False)
    cnt_25 = models.IntegerField(blank=False, null=False)
    cnt_20 = models.IntegerField(blank=False, null=False)
    cnt_6 = models.IntegerField(blank=False, null=False)
    close_order_time = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return str(self.ticket)

class LoadingLog(models.Model): #logs live data from devices at location- loading
    counter = models.ForeignKey(Counter, on_delete=models.PROTECT,null=True, blank=True)
    category = models.ForeignKey(WeightCategory, on_delete=models.PROTECT)
    weight = models.DecimalField(decimal_places=2,max_digits=30,blank=False)
    bag_cnt = models.IntegerField(blank=False)
    device = models.CharField(blank=False, max_length=15)  # data is from which device
    order = models.CharField(blank=False, max_length=8, null=False)
    created =  models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.device) + " " + str(self.category) + " " + str(self.bag_cnt)
    




