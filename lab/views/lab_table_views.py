from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from django_tables2 import SingleTableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils.http import urlencode
from lab.models import COA
from lab.tables import COAListTAble
from lab.filters import COAListFilter

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        print(self.request.user.username)
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context

class COATableView(LoginRequiredMixin,PagedFilteredTableView):
    model = COA
    paginate_by = 14
    queryset = COA.objects.all().order_by("-sampling_date")
    table_class = COAListTAble
    filter_class = COAListFilter
    template_name = "lab/coa-list-table-new.html"


