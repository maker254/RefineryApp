from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
import datetime
from datetime import timedelta, datetime
from sales.models import LoadingLog
from dbmaster.models import WeightCategory
from dbmaster.forms import DateForm

def dailyLoadingReport(request):
    form = DateForm
    report_day = timezone.now()  #returns now time in UTC
    time_diff = 3  #timedifferrence btwn UTC and EAT
    report_day_local_tz = report_day + timedelta(hours = time_diff) #convert to localtimezone EAT
    report_date_local = report_day_local_tz.date()
    report_hr_local = int(report_day_local_tz.hour)
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            report_date = form.cleaned_data['date']
            if ( report_date != timezone.now().date() ):
                day_end_time = datetime.max.time()
                report_day = datetime.combine(report_date, day_end_time)
                report_day_local_tz = report_day   #no need to account for timediff as datetime is already in UTC
                report_date_local = report_day_local_tz.date()
                report_hr_local = report_day_local_tz.hour
    hours_dict = (
        '00:00 - 01:00','01:00 - 02:00','02:00 - 03:00','03:00 - 04:00','04:00 - 05:00','05:00 - 06:00','06:00 - 07:00',
        '07:00 - 08:00','08:00 - 09:00','09:00 - 10:00','10:00 - 11:00','11:00 - 12:00','12:00 - 13:00','13:00 - 14:00',
        '14:00 - 15:00','15:00 - 16:00','16:00 - 17:00','17:00 - 18:00','18:00 - 19:00','19:00 - 20:00','20:00 - 21:00',
        '21:00 - 22:00','22:00 - 23:00','23:00 - 00:00',   
        )
    daily_weight_total = 0
    loading_details = []
    categories =  WeightCategory.objects.all()
    for i in range (0,report_hr_local+1): #plus one so as to also include data from current hour
        """UTC time is 3hrs behind EAT.
          Thus the first hour of todays date in localtimezone(i.e 00:00), is saved as 21:00 of yesterdays date in the database(db is in UTC TIME) """
        db_datetime = report_day_local_tz - timedelta(hours= time_diff + report_hr_local - i )
        hour_prefix = hours_dict[i - time_diff]
        hour_range = hours_dict[i]
        hour_weight_total = 0
        hour_bags_count = 0
        hour_data = []
        for category in categories:
            data = LoadingLog.objects.filter(created__icontains = str(db_datetime.date()) ).filter(created__icontains = str(db_datetime.date()) + " " + str(hour_prefix[0:2]), category=category)
            hour_weight_total = hour_weight_total + ( data.count() * int(category.category[:-2]) )
            hour_bags_count = hour_bags_count + data.count()
            hour_data.append({str(category):[data.count(),data.count() * int(category.category[:-2])]})
        loading_details.append({str(hour_range):[hour_data,hour_weight_total]})
        daily_weight_total += hour_weight_total
    return render(request, 'sales/daily-loading-report.html',{'details':loading_details, 'dailyWeightTotal':daily_weight_total, 'date':report_date_local, 'form':form})