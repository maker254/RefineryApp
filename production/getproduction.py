#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import message
from itertools import count
import socket
from socket import *
import time
import re

from production.models import DataLog
from dbmaster.models import WeightCategory

def call_arduino():
    address = ('10.4.0.90', 5000)
    try:
        data = 'Batch-Count' #SlaveBatchCount alternative so as to compare perfomance speed
        client_socket = socket(AF_INET, SOCK_DGRAM) #set up the socket
        client_socket.settimeout(2) #only wait 1 second for a response 
        client_socket.sendto(data.encode(), address) #send command to arduino
        rec_data, addr = client_socket.recvfrom(2048) #read response from arduino
        message=rec_data.decode()#string from arduino indicating logic 0 or 1 to show detection of object
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

def get_production_data(message, category):
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
    print( str(category)+': count:'+str(count_data)+' TWeight:'+str(weight_data) )

    context = {
        'category':category,
        'count_data':count_data,
        'weight_data':weight_data,
        'status':'ok'
    }
    return context
    
def datalog():
    context = call_arduino()
    status = context.get('status')
    categories =['50kg','25kg','20kg','6kg']
    for category in categories:
        print(category)
        category = WeightCategory.objects.get(category=category)
        if DataLog.objects.filter(category=category).count()==0:
           DataLog(category=category,weight=0,bag_cnt=0).save()
    if status == 'ok':
        message = context.get('message')
        for category in categories:
            context = get_production_data(message, category)
            count_data = int( context.get('count_data') )
            weight_data = float( context.get('weight_data') )
            category = WeightCategory.objects.get(category=category)
            if DataLog.objects.filter(category=category,weight=weight_data,bag_cnt=count_data).exists():
                pass
            else:
                DataLog(category=category,weight=weight_data,bag_cnt=count_data).save()
    return context
