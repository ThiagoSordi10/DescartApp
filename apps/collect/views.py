from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView
from django.http import HttpResponseRedirect
from .models import Demand, Address, AddressDemand
from .forms import DemandForm
from core.models import Collector

class BaseDemand():

    context_object_name = "demand"
    model = Demand
    success_url = reverse_lazy("list_demand")

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        try: 
            user = Collector.objects.get(user = self.request.user)
            return handler
        except Collector.DoesNotExist:
            raise PermissionDenied


class BaseAddress():

    context_object_name = "address"
    model = Address
    success_url = reverse_lazy("list_demand")


# class BaseDetailDemand(BaseDemand):

    # def test_func(self):
    #     try: 
    #         user = Collector.objects.get(user = self.request.user)
    #         return True
    #     except Collector.DoesNotExist:
    #         raise PermissionDenied


@method_decorator(login_required, name='dispatch')
class DemandCreateView(BaseDemand, CreateView):

    form_class = DemandForm
    template_name = "demand/new.html"

    def get_form_kwargs(self):
        kwargs = super(DemandCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        demand = form.save(commit = False)
        demand.collector = self.request.user.collector
        demand.save()
        for address in form.cleaned_data['addresses']:
            AddressDemand.objects.create(address=address, demand=demand)
        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class DemandListView(BaseDemand, ListView):

    template_name = "demand/list.html"


    def get_queryset(self):
        return Demand.objects.filter(collector=self.request.user.collector).distinct()
