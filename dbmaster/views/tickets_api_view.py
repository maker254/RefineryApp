from django.http import HttpResponse
from django.shortcuts import render
from main import settings
import requests
from django.contrib.auth.decorators import login_required,permission_required

import logging
from rest_framework import viewsets
from dbmaster.serializers import TicketSerializer
from dbmaster.models import Ticket

class TicketApiViewSet(viewsets.ModelViewSet):
    #queryset=Ticket.objects.filter(has_order=True,loaded=False).all().order_by('has_order_time')
    queryset=Ticket.objects.all()
    serializer_class=TicketSerializer

@login_required(login_url='/accounts/login/')
def get_tickets_api(request):
    try:
        wb_response = requests.get("http://10.4.1.176:80/dbmaster/api-tickets/")
        ksl_wb_data = wb_response.json()
        saving_dict={}
        ticket_instance=Ticket()
        for ticket_data in  ksl_wb_data:
            for key,data in ticket_data.items():
                saving_dict[key]=data
            ticket_instance=Ticket(**saving_dict)
            # checked_saved=Ticket.objects.filter(vehicle_no=saving_dict['Vehicle Number']).count()
            # if checked_saved >0:
            #     Ticket.objects.filter(vehicle_no=saving_dict['Vehicle Number']).update(**saving_dict)
            # else:
            #     ticket_instance.save()
        queryset=Ticket.objects.all()
        return render(request, 'dbmaster/ticket_master.html',{'data':queryset})
    except Exception as e:
        print(e)
        return HttpResponse('An error occurred')
    

