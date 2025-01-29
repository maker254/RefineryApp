from django.contrib import admin
from .models import PumpHouse,Pump,PumpLog
# Register your models here.

@admin.register(PumpHouse)
class PumpHouseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Pump)
class PumpAdmin(admin.ModelAdmin):
    list_display = ('pumphouse','code',)

@admin.register(PumpLog)
class PumpLogAdmin(admin.ModelAdmin):
    list_display = ('pump','running_hrs','created')