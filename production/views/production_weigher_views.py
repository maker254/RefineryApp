from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

from production.models import DataLog
from dbmaster.models import WeightCategory

# Create your views here.

class LiveProductionView(TemplateView):
    template_name = 'production/live-production.html'

def send_production_json(request):
    categories = WeightCategory.objects.all()
    for category in categories:
        if DataLog.objects.filter(category=category).exists():
            pass
        else:
            DataLog(category=category,weight=0, bag_cnt=0).save()
     
    data_50kg = DataLog.objects.filter(category__category='50kg').latest('id')
    count_50kg = data_50kg.bag_cnt
    tweight_50kg =  count_50kg * 50 # data_50kg.weight
    
    data_25kg = DataLog.objects.filter(category__category='25kg').latest('id')
    count_25kg = data_25kg.bag_cnt
    tweight_25kg = count_25kg * 25 # data_25kg.weight

    data_20kg = DataLog.objects.filter(category__category='20kg').latest('id')
    count_20kg = data_20kg.bag_cnt
    tweight_20kg = count_20kg * 20 # data_20kg.weight
    
    data_6kg = DataLog.objects.filter(category__category='6kg').latest('id')
    count_6kg = data_6kg.bag_cnt
    tweight_6kg = count_6kg * 6 # data_6kg.weight
  
    context = {
        'count_50kg':count_50kg,
        'count_25kg':count_25kg,
        'count_20kg':count_20kg,
        'count_6kg':count_6kg,
        'tweight_50kg':tweight_50kg,
        'tweight_25kg':tweight_25kg,
        'tweight_20kg':tweight_20kg,
        'tweight_6kg':tweight_6kg,
        }
    return JsonResponse(context, safe=False)
