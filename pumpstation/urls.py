from django.urls import include, path
from . import views
from .views import pumpStationMap,getPumpRunningHrs

app_name = "pumpstation"
urlpatterns = [
    path('maps/', views.pumpStationMap, name='maps'),
    path('get-pump-data/<str:pumphouse>/', views.getPumpRunningHrs, name='get-pump-data')
]