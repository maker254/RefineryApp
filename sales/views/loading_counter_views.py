import time
import json
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView,ListView,UpdateView,CreateView
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from sales.models import LoadingLog
from dbmaster.models import WeightCategory,Device,Ticket
from sales.models import Counter,ServedOrder
from sales.forms import CounterCreateForm,CounterUpdateForm,SetCounterForm
from sales.getloading import call_arduino

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def send_loading_json(request):
    counter_list = [ counter.pk for counter in Counter.objects.all()]
    categories = WeightCategory.objects.all()
    context = {}
    for item in counter_list:
        counter = Counter.objects.get(pk=item)
        count_data = []
        for category in categories:
            if LoadingLog.objects.filter(category=category,counter=counter,order__icontains=counter.ticket.vehicle_no).exists():
                count_data.append( LoadingLog.objects.filter(category=category,counter=counter,order__icontains=counter.ticket.vehicle_no).latest("id").bag_cnt )
            else:
                count_data.append(0)
        context[item] = {
                    '50kg':count_data[0],
                    '25kg':count_data[1],
                    '20kg':count_data[2],
                    '6kg':count_data[3],
                    }
    return JsonResponse(context, safe=False)

# def send_loading_json(request):
#     counter_list = [ counter.device.location.conveyor_code for counter in Counter.objects.all()]
#     categories = WeightCategory.objects.all()
#     context = {}
#     for item in counter_list:
#         device = Device.objects.get(location__location_name="Loading",location__conveyor_code=item)
#         counter = Counter.objects.get(device__location__conveyor_code=item)
#         count_data = []
#         for category in categories:
#             if LoadingLog.objects.filter(category=category,device=device.ip, order__icontains=counter.ticket.vehicle_no).exists():
#                 count_data.append( LoadingLog.objects.filter(category=category,device=device.ip, order__icontains=counter.ticket.vehicle_no).latest("id").bag_cnt )
#             else:
#                 count_data.append(0)
#         context[item] = {
#                     '50kg':count_data[0],
#                     '25kg':count_data[1],
#                     '20kg':count_data[2],
#                     '6kg':count_data[3],
#                     }
#     return JsonResponse(context, safe=False)


class CounterListView(ListView):
    model = Counter
    queryset = Counter.objects.all().order_by("device__location__conveyor_code")
    form = SetCounterForm
    template_name = "sales/counter-list-table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class CounterCreateView(LoginRequiredMixin,CreateView):
    model = Counter
    form_class = SetCounterForm
    template_name = "sales/counter-create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context = self.request.POST
        return context
    
    def form_valid(self, form):
        context = super().get_context_data()
        if form.is_valid:
            form.instance = form.save()
            messages.success(self.request,"Counter Added Successfully")
            return redirect('sales:counter-list') 
        else:
            messages.warning(self.request, "Counter Couldn't be added")
            return super().form_invalid(form)
    def get_success_url(self):
        return reverse("sales:counter-update",kwargs={'pk':self.kwargs['pk']})

class CounterUpdateView(LoginRequiredMixin,UpdateView):
    model = Counter
    form_class = CounterUpdateForm
    template_name = "sales/counter-update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context = self.request.POST
        if self.request.method == 'GET':
            if self.object.is_running:
                messages.error(self.request, "Updating Counter Not Allowed While Counter is ON ")
        return context
    
    def form_valid(self, form):
        context = super().get_context_data()
        if form.is_valid:
            form.instance = form.save()
            messages.success(self.request, "Counter Updated Successfully")
        return redirect('sales:counter-list')  #redirect back to counter list 
    def get_success_url(self):
        return reverse("sales:counter-update",kwargs={'pk':self.kwargs['pk']})

@login_required(login_url='/accounts/login')
def startCounter(request, **kwargs):
    data=[]
    mimetype = "application/json"
    if is_ajax(request):
        toggleState = request.GET['toggleState']
        counter = Counter.objects.get(id=kwargs['pk'])
        device = counter.device
        results = []
        for i in range (0,5):
            if toggleState == "ON":
                is_running = True
                order_details = str(counter.ticket.vehicle_no)+ " 50kg:"  + str(counter.order_50) + " 25kg:" + str(counter.order_25) + " 20kg:" + str(counter.order_20) + " 6kg:" + str(counter.order_6) 
                ard_context = call_arduino(device, "Order:"+ str(order_details))
            if toggleState == "OFF":
                ard_context = call_arduino(device,"STOP")
                is_running = False
            if ard_context.get('status') == 'ok':
                Counter.objects.filter(id=kwargs['pk']).update(is_running=is_running)
                results.append({"is_running":is_running})
                data=json.dumps(results)
                return HttpResponse(data, mimetype)
            time.sleep(0.2) 
        results.append({"is_running":None}) 
    data=json.dumps(results)                             
    return HttpResponse(data, mimetype)

@login_required(login_url='/accounts/login')
def closeCounter(request, pk):
    counter = get_object_or_404(Counter, pk=pk)
    if request.method=='POST':
        if counter.is_running:
            messages.error(request, "Closing Counter Not Allowed While ON ")
        else:
            messages.success(request,"Counter Closed ")
            Ticket.objects.filter(pk=counter.ticket.pk).update(loaded=True,loaded_time=timezone.now())
            ServedOrder(ticket=counter.ticket,counter_no=counter,cnt_50=counter.order_50,cnt_25=counter.order_25,
                        cnt_20=counter.order_20,cnt_6=counter.order_6,close_order_time=timezone.now(),
                        loaded_quantity=(counter.order_50*50)+(counter.order_25*25)+(counter.order_20*20)+(counter.order_6*6)).save()
            Counter.objects.filter(pk=pk).update(closed=True) #close counter
    return redirect ('sales:counter-list')

@login_required(login_url='/accounts/login')
def setCounter(request):
    form = SetCounterForm
    print("set counter view called")
    if request.method == 'POST':
        form = SetCounterForm(request.POST)
        if form.is_valid():
            device = form.cleaned_data['device']
            ticket = form.cleaned_data['ticket']
            order_50 = form.cleaned_data['order_50']
            order_25 = form.cleaned_data['order_25']
            order_20 = form.cleaned_data['order_20']
            order_6 = form.cleaned_data['order_6']
            Counter.objects.filter(device=device).update(ticket=ticket,order_50=order_50,order_25=order_25,order_20=order_20,
                                                         order_6=order_6,closed=False,is_running=False)
            messages.success(request, "counter " + str(device) + " Set" )
        else:
            messages.error(request, "!!Error!! Could Not Set Counter")
            print(form.errors)
    return redirect ('sales:counter-list')
    
