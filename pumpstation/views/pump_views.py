import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pumpstation.forms import googleMapSearchForm
from pumpstation.models import Pump,PumpHouse,PumpLog

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def pumpStationMap(request):
    form = googleMapSearchForm
    return render(request, "pumpstation/maps-new.html", {"form":form})

def getPumpRunningHrs(request, **kwargs):
    data = []
    if is_ajax(request):
        pumphouse = kwargs['pumphouse']
        print(pumphouse)
        pumps = Pump.objects.filter(pumphouse__name__contains=pumphouse)
        for pump in pumps: 
            pumpdata = PumpLog.objects.filter(pump=pump).latest("id")  
            data.append({'code':pumpdata.pump.code, 'running_hrs':pumpdata.running_hrs})
    return JsonResponse(data, safe=False)
    