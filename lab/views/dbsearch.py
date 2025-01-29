import json
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from lab.models import COA

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_coas(request):
    data = []
    if is_ajax(request):
        term = request.GET.get("term", "")
        coas = COA.objects.filter(Q(batch_no__icontains = term)|Q(sample__name__icontains=term)|Q(brand__name__icontains=term)).all()
        results = []
        for coa in coas:
            new_row = {}
            new_row['label'] = str(coa.batch_no) + ' ' + str(coa.brand.name) + ' ' + str(coa.sampling_date)
            new_row['value'] = coa.id 
            results.append(new_row)
            data=json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

def get_coa_details(request):
    data = {'sample':[], 'brand':[], 'sampling_date':[], 'manufacture_date':[], 'analysis_date':[], 'expiry_date':[], 'batch_no':[],  'sodium_chloride':[], 'calcium':[], 'magnesium':[], 'sulphates':[], 'alkalinity':[], 'iodine':[], 'insoluble_matter':[], 'moisture_content':[], 'sieve_size':[],
            'sodium_chloride_eas':[], 'calcium_eas':[], 'magnesium_eas':[], 'sulphates_eas':[], 'alkalinity_eas':[], 'iodine_eas':[], 'insoluble_matter_eas':[], 'moisture_content_eas':[], 'sieve_size_eas':[], }
    q = request.GET.get("code", "")
    coa_details = COA.objects.filter(id=q)
    for coa in coa_details:
        expiry_date = get_expiry_date(coa.sampling_date)
        data['sample'].append(coa.sample.name)
        data['brand'].append(coa.brand.name)
        data['sampling_date'].append(coa.sampling_date)
        data['analysis_date'].append(coa.analysis_date)
        data['manufacture_date'].append(coa.sampling_date.strftime('%B') + ' ' + str(coa.sampling_date.year))
        data['expiry_date'].append(expiry_date.strftime('%B') + ' ' + str(expiry_date.year))
        data['batch_no'].append(coa.batch_no)
        data['sodium_chloride'].append(coa.chloride)
        data['calcium'].append(coa.calcium)
        data['magnesium'].append(coa.magnesium)
        data['sulphates'].append(coa.sulphates)
        data['alkalinity'].append(coa.alkalinity)
        data['iodine'].append(coa.iodine)
        data['insoluble_matter'].append(coa.insoluble_matter)
        data['moisture_content'].append(coa.moisture)
        data['sieve_size'].append(coa.sieve_size)
        data['sodium_chloride_eas'].append( str( int (coa.eas.chloride) ) + 'Min')
        data['calcium_eas'].append( str(coa.eas.calcium) + 'Max')
        data['magnesium_eas'].append( str(coa.eas.magnesium) + 'Max')
        data['sulphates_eas'].append( str(coa.eas.sulphates) + 'Max')
        data['alkalinity_eas'].append( str(coa.eas.alkalinity) + 'Max') 
        data['iodine_eas'].append(str( int(coa.eas.iodine_min) ) + 'mg/Kg(Min) - ' + str( int(coa.eas.iodine_max) ) + 'mg/Kg(Max)' )
        data['insoluble_matter_eas'].append( str(coa.eas.insoluble_matter) + 'Max')
        data['moisture_content_eas'].append( str( int(coa.eas.moisture) ) + 'Max')
        data['sieve_size_eas'].append( str(coa.eas.sieve_size) )
    return JsonResponse(data, safe=True)

def get_expiry_date(samplingdate):
    expiry_date = samplingdate + relativedelta(months=35) #expires 35 months after date of manufacture/sampling
    return expiry_date

