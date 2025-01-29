from django.urls import include, path
from . import views
from sales.views import (send_loading_json,dailyLoadingReport,
                         CounterListView,CounterCreateView,CounterUpdateView,
                         startCounter,closeCounter,setCounter)

app_name="sales"
urlpatterns = [
    path("loading-json/",send_loading_json, name="loading-json"),
    path("daily-loading-report/", dailyLoadingReport, name="daily-loading-report"),

    path("counter-list/", CounterListView.as_view(), name="counter-list"),
    path("counter-update/<int:pk>/", CounterUpdateView.as_view(), name="counter-update"),
    path("counter-create/", CounterCreateView.as_view(), name="counter-create"),

    path("start-counter/<int:pk>/", startCounter, name="start-counter"),
    path("counter-delete/<int:pk>/", closeCounter, name="counter-delete"),
    path("set-counter/",setCounter, name="set-counter"),
    
]