import requests
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from lab.forms import COAForm,COAPrintForm,COAFormset
from lab.models import COA,EAS

from main.settings import BASE_DIR


class COAMultipleCreateView(LoginRequiredMixin,CreateView):
    model = COA
    form_class = COAForm
    COA_details = COAFormset
    template_name = "lab/coa-create-multiple-new.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['COA_details'] = self.COA_details()
        return data
    
    def post(self, request,*args,**kwargs):
        formsets = self.COA_details(self.request.POST)
        if formsets.is_valid():
            print("valid formsets")
            return self.form_valid(formsets)
        return self.form_invalid(request,formsets)
    
    def form_valid(self, formsets):
        user = self.request.user
        for formset in formsets:
            if formset.cleaned_data.get('brand') and formset.cleaned_data.get('sampling_date'):
                instance = formset.save(commit=False)
                if instance.brand.name == "DRIED IODIZED COARSE SALT":
                    eas_specification =  EAS.objects.get(name="COARSE SALT")
                else:
                    eas_specification =  EAS.objects.get(name="REFINED SALT")
                instance.eas = eas_specification
                instance.analysis_date = formset.cleaned_data.get('sampling_date')
                instance.modified_by = user.username
                instance.save()
        messages.success(self.request, 'COA data added successfully')
        return  HttpResponseRedirect(reverse('lab:coa-list') )
    
    def form_invalid(self, request, formsets):
        messages.error(self.request, formsets.errors)
        return render(request, self.template_name, {'COA_details': formsets})


#create one record at a time
class COACreateView(LoginRequiredMixin,CreateView):
    model = COA
    form_class = COAForm
    template_name = "lab/coa-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context = self.request.POST
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        if form.is_valid():
            form.instance = form.save(commit=False)
            form.instance.modified_by = user.username
            if form.instance.brand.name == "DRIED IODIZED COARSE SALT":
                eas_specification =  EAS.objects.get(name="COARSE SALT")
            else:
                eas_specification =  EAS.objects.get(name="REFINED SALT")
                form.instance.eas = eas_specification
            form.save()
            messages.success(self.request, 'COA data added successfully')
            
        else:
            messages.warning(self.request, 'Error saving data')
        return super().form_valid(form)


class COAUpdateView(LoginRequiredMixin,UpdateView):
    model = COA
    form_class = COAForm
    template_name = "lab/coa-update.html"  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eas'] = EAS.objects.get(id=self.object.eas.id)
        if self.request.method == 'POST':
            context = self.request.POST
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        if form.is_valid():
            form.instance = form.save(commit=False)
            form.instance.modified_by =  user.username
            form.save()
            messages.success(self.request, 'COA data updated successfully')
        else:
            messages.warning(self.request, 'Error saving data')
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("lab:coa-details",kwargs={'pk':self.kwargs['pk']})
    
class COADetailView(LoginRequiredMixin,DetailView):
    model = COA
    template_name = "lab/coa-detail.html"

@login_required(login_url='/accounts/login')
def coa_print_view(request):
    form = COAPrintForm
    return render(request, 'lab/coa-print.html', {'form':form})

#Function based create multiple
@login_required(login_url='/accounts/login')
def coa_create_multiple(request):
    if request.method == 'POST':
        formsets = COAFormset(request.POST)
        print(formsets.errors)
        eas = EAS.objects.latest('id')
        for formset in formsets:
            if formset.is_valid(): 
                #instances = formsets.save(commit=False
                # )
                #only try saving if this is there
                if formset.cleaned_data.get('brand') and formset.cleaned_data.get('sampling_date'):
                    instance = formset.save(commit=False)
                    print(instance)
                    instance.eas = eas 
                    instance.save()
    formsets = COAFormset
    return render(request, 'lab/coa-create-multiple.html', {'COA_details':formsets}) 
