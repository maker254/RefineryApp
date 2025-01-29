from django.db import models

# Create your models here.
class PumpHouse(models.Model):
    name = models.CharField(max_length=12, blank=False)
    latitude = models.CharField(max_length=12, blank=True)
    longitude = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return str(self.name) 
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name',], name='unique_pumphouse')
               ]
        
class Pump(models.Model):
    pumphouse = models.ForeignKey(PumpHouse, on_delete=models.PROTECT)
    code = models.CharField(max_length=10, blank=False)
    latitude = models.CharField(max_length=12, blank=True)
    longitude = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return str(self.code) 
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code',], name='unique_pump')
               ]


class PumpLog(models.Model):
    pump = models.ForeignKey(Pump, on_delete=models.PROTECT)
    running_hrs = models.DecimalField(max_digits=8,decimal_places=2,blank=False)
    created = models.DateTimeField(auto_now_add=True)