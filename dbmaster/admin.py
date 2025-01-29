from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from dbmaster.models import *

class NavSubMenuInline(admin.TabularInline):
      model=NavSubMenu

@admin.register(NavMainMenu)
class NavMenuAdmin(admin.ModelAdmin):
      inlines = [
        NavSubMenuInline, 
        ]
      
@admin.register(WeightCategory)
class WeightCategoryAdmin(admin.ModelAdmin):
      list_display = ('category',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name','conveyor_code',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
      list_display=('ip',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
      list_display=('vehicle_no',)
