#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import count
import socket
from socket import *
import time
import re
from dbmaster.models import WeightCategory,Device
from sales.models import LoadingLog


def call_arduino(device, context):
    address = (device.ip, device.port)
    try:
        data = context
        client_socket = socket(AF_INET, SOCK_DGRAM) #set up the socket
        client_socket.settimeout(0.5) #only wait 1 second for a response 
        client_socket.sendto(data.encode(), address) #send command to arduino
        rec_data, addr = client_socket.recvfrom(2048) #read response from arduino
        message=rec_data.decode()#string from arduino indicating logic 0 or 1 to show detection of object
        print(message)

        context = {
            'message':message,
            'status':'ok'
        }
    except:
        context = {
            'message':' ',
            'status':'Error'
        }
    return context

def get_loading_data(message, category):
    category = category
    start = message.find(category)
    end = message.find(';', start +1)
    category_data = message[start:end]

    count_start = category_data.find('Count:')
    count_end = category_data.find('Weight:', count_start)
    count_data = category_data[count_start+6:count_end]
    
    weight_start = category_data.find('Weight:')
    weight_end = category_data.find('Category', weight_start)
    weight_data = category_data[weight_start+7:]

    vehicle_start = message.find("Vehicle_no:")
    vehicle_end = message.find("Device", vehicle_start)
    vehicle_data = message[vehicle_start+11:vehicle_end-2]

    device_start = message.find("Device:")
    device_data = message[device_start+7:-1]

    print(str(device_data) + 'Vehicle_no:' + str(vehicle_data) + 'Category:' + str(category)+': count:'+str(count_data)+' TWeight:'+str(weight_data) )

    context = {
        'category':category,
        'count_data':count_data,
        'weight_data':weight_data,
        'vehicle_data':vehicle_data,
        'device_data':device_data,
        'status':'ok'
    }
    return context

def datalog(pk):
    device = Device.objects.get(pk=pk)
    context = call_arduino(device, "Batch-Count")
    status = context.get('status')
    categories =[ item.category for item in WeightCategory.objects.distinct]
    for category in categories:
        if LoadingLog.objects.filter(category=category).count()==0:
           LoadingLog(category=category,weight=0,bag_cnt=0,device="initialize_db",order="initialize_db").save()
    if status == 'ok':
        message = context.get('message')
        for category in categories:
            context = get_loading_data(message, category)
            count_data = int( context.get('count_data') )
            weight_data = float( context.get('weight_data') )
            vehicle_data = context.get('vehicle_data')
            device_data = context.get('device_data')
            #category = WeightCategory.objects.get(category=category)
            if LoadingLog.objects.filter(category=category,bag_cnt=count_data,order=vehicle_data).exists():
                pass
            else:
                LoadingLog(category=category,weight=weight_data,bag_cnt=count_data,order=vehicle_data,device=device_data).save()
    return context

