from django.contrib import admin
from sales.models import ServedOrder,LoadingLog,Counter

# Register your models here.

@admin.register(ServedOrder)
class ServedOrderAdmin(admin.ModelAdmin):
    list_display = ("counter_no","ticket","loaded_quantity")

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    pass

@admin.register(LoadingLog)
class LoadingLogAdmin(admin.ModelAdmin):
    list_display = ("counter","order","category","bag_cnt","weight","created")
    list_filter = ("counter","order","category")