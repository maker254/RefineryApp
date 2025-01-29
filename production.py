import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
import django
django.setup()
import time
from production.getproduction import datalog
# import schedule

# #schedule.every(1).minutes.do(get_daily_hourly_report)
# #schedule.every().day.at("00:00").do(get_daily_hourly_report)

while True:
    datalog()
    #schedule.run_pending()
    time.sleep(1)
