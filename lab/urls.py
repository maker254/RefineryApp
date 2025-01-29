from django.urls import include, path
from lab.views import (COACreateView,COATableView,COAUpdateView,COAMultipleCreateView,COADetailView,
                        coa_print_view,get_coas,get_coa_details)
from . import views

app_name="lab"
urlpatterns = [
    path('add&print-coa/', COACreateView.as_view(), name='add&print-coa'),
    path('coa-create-multiple', COAMultipleCreateView.as_view(), name="coa-create-multiple"),
    path('coa-list/', COATableView.as_view(), name='coa-list'),
    path('<int:pk>/coa-details/', COADetailView.as_view(), name='coa-details'),
    path('<int:pk>/coa-update/', COADetailView.as_view(), name='coa-update'),

    path('json/coas-autocomplete/', views.get_coas, name='coas-autocomplete'),
    path('json/get-coa-details/', views.get_coa_details, name= 'get-coa-details'),
]