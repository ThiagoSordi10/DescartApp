from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from .models import Demand, Address
from .forms import DemandForm
from core.models import Collector

class BaseDemand():

    context_object_name = "demand"
    model = Demand
    success_url = reverse_lazy("demands_list")


class BaseAddress():

    context_object_name = "address"
    model = Address
    success_url = reverse_lazy("demands_list")


class BaseDetailDemand(BaseDemand""", UserPassesTestMixin"""):

    # def test_func(self):
    #     try: 
    #         user = Collector.objects.get(user = self.request.user)
    #         return True
    #     except Collector.DoesNotExist:
    #         return False

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        try: 
            user = Collector.objects.get(user = self.request.user)
            return handler
        except Collector.DoesNotExist:
            raise PermissionDenied

@method_decorator(login_required, name='dispatch')
class DemandCreateView(BaseDemand, CreateView):

    form_class = DemandForm
    template_name = "demand/new.html"
