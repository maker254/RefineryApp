from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

from production.models import ProductionCounter,ProductionLog
from dbmaster.models import WeightCategory

# Create your views here.

class ProductionCounterListView(ListView):
    model = ProductionCounter
    queryset = ProductionCounter.objects.all().order_by("device__location__conveyor_code")
    template_name = "production/counter-list-table.html"

def send_production_json(request):
    categories = WeightCategory.objects.all()
    counters = ProductionCounter.objects.all()
    context = {}
    for counter in counters:
        count_data = []
        for category in categories:
            if ProductionLog.objects.filter(counter=counter,category=category).exists():
                count_data.append( ProductionLog.objects.filter(category=category,counter=counter).latest("id").bag_cnt )
            else:
                count_data.append(0)
                # ProductionLog(counter=counter,category=category,weight=0, bag_cnt=0).save()
        context[counter.id] = {
                '50kg':count_data[0],
                '25kg':count_data[1],
                '20kg':count_data[2],
                '6kg':count_data[3],
                }
    return JsonResponse(context, safe=False)
