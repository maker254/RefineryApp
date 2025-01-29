from django.urls import include, path
from production.views import ProductionCounterListView,send_production_json,dailyProductionReport
from . import views

app_name="production"
urlpatterns = [
    path('production-live/', ProductionCounterListView.as_view(), name='production-live'),
    path('send-production-json/', send_production_json, name='send-production-json'),
    path('daily-production-report/', views.dailyProductionReport, name="daily-production-report")
]