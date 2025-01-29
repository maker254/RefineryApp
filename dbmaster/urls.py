from django.urls import include, path
from rest_framework import routers
from dbmaster.views import TicketApiViewSet
from .views import *

router=routers.DefaultRouter()
router.register(r'api-tickets',TicketApiViewSet)

app_name = 'dbmaster'
urlpatterns = [
    #API
    path('', include(router.urls)),
    path('get_tickets/', get_tickets_api, name='get_tickets'),
    
]