from django.contrib import admin
from production.models import ProductionCounter,ProductionLog

# Register your models here.

@admin.register(ProductionCounter)
class ProductionCounterAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ('counter','category','weight','bag_cnt','created')
    list_filter = ('counter','category','created')
