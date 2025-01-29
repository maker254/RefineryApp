import time
import json
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView,ListView,UpdateView,CreateView
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from sales.models import LoadingLog
from dbmaster.models import WeightCategory,Device
from sales.models import Counter
from sales.forms import CounterCreateForm,CounterUpdateForm
from sales.getloading import sendOrderDetailToArduino

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def send_loading_json(request):
    counter_list=[]
    for counter in  Counter.objects.all():
        counter_list.append(counter.device.location.conveyor_code)
    categories = WeightCategory.objects.all()
    context = {}
    for item in counter_list:
        device = Device.objects.get(location__conveyor_code=item)
        counter = Counter.objects.get(device__location__conveyor_code=item)
        for category in categories:
            if LoadingLog.objects.filter(category=category,device=device.ip).exists():
                pass
            else:
                LoadingLog(category=category,weight=0, bag_cnt=0, device=device.ip).save() 

        count_50kg = LoadingLog.objects.filter(category__category='50kg',device=device.ip, order__icontains=counter.ticket.vehicle_no).count()
        count_25kg = LoadingLog.objects.filter(category__category='25kg',device=device.ip, order__icontains=counter.ticket.vehicle_no).count()
        count_20kg = LoadingLog.objects.filter(category__category='20kg',device=device.ip, order__icontains=counter.ticket.vehicle_no).count()
        count_6kg = LoadingLog.objects.filter(category__category='6kg',device=device.ip, order__icontains=counter.ticket.vehicle_no).count()
        context[item] = {
                    '50kg':count_50kg,
                    '25kg':count_25kg,
                    '20kg':count_20kg,
                    '6kg':count_6kg,
                    }
    return JsonResponse(context, safe=False)


class CounterListView(ListView):
    model = Counter
    queryset = Counter.objects.all().order_by("device__location__conveyor_code")
    template_name = "sales/counter-list-table.html"

class CounterCreateView(LoginRequiredMixin,CreateView):
    model = Counter
    form_class = CounterCreateForm
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
                beltstate = "Belt RUNNING"
                is_running = True
                order_qty = counter.order_50 + counter.order_25 + counter.order_20 + counter.order_6
                order_details = str(counter.ticket.vehicle_no)+ " 50kg:"  + str(counter.order_50) + " 25kg:" + str(counter.order_25) + " 20kg:" + str(counter.order_20) + " 6kg:" + str(counter.order_6) 
                ard_context = sendOrderDetailToArduino(device, "Order:"+ str(order_details))
            if toggleState == "OFF":
                ard_context = sendOrderDetailToArduino(device,"STOP")
                beltstate = "Belt STOPPED"
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
            counter.delete()
    return redirect ('sales:counter-list')
