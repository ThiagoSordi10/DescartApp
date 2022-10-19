from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, UpdateView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Demand, Address, AddressDemand
from .forms import DemandForm, DemandUpdateForm, DemandAddressesForm
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


class BaseDetailDemand(BaseDemand):

    def dispatch(self, request, *args, **kwargs):
        try:
            super(BaseDetailDemand, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object.collector != request.user.collector:
                raise PermissionDenied
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except PermissionDenied:
            raise PermissionDenied


@method_decorator(login_required, name='dispatch')
class DemandCreateView(BaseDemand, CreateView):

    form_class = DemandForm
    template_name = "demand/form.html"
    extra_context = {
        "method": "Create"
    }

    def form_valid(self, form):
        demand = form.save(commit = False)
        demand.collector = self.request.user.collector
        demand.save()
        return HttpResponseRedirect(reverse_lazy("demand_address", args=[demand.id]))


@method_decorator(login_required, name='dispatch')
class DemandListView(BaseDemand, ListView):

    template_name = "demand/list.html"
     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        demands = Demand.objects.filter(collector=self.request.user.collector).distinct()

        paginator = Paginator(demands, 6)
        page = self.request.GET.get('page')
        demands_page = paginator.get_page(page)

        context['demand_list'] = demands_page
        return context


@method_decorator(login_required, name='dispatch')
class DemandUpdateView(BaseDetailDemand, UpdateView):

    form_class = DemandUpdateForm
    template_name = "demand/form.html"
    extra_context = {
        "method": "Update"
    }

    def form_valid(self, form):
        demand = form.save(commit = True)
        return HttpResponseRedirect(reverse_lazy("demand_address", args=[demand.id]))

# @method_decorator(login_required, name='dispatch')
# class DemandDeleteView(BaseDetailCaptacao, DeleteView):

#     template_name = "captacoes/delete.html"

@method_decorator(login_required, name='dispatch')
class DemandAddressesView(BaseDemand, UpdateView):

    form_class = DemandAddressesForm
    template_name = "demand/demand_address.html"

    def get_form_kwargs(self):
        kwargs = super(DemandAddressesView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs.update(self.kwargs)
        return kwargs

    def form_valid(self, form):
        demand_id = self.kwargs.pop("pk")
        for address in form.cleaned_data['addresses']:
            AddressDemand.objects.create(address=address, demand_id=demand_id)
        AddressDemand.objects.filter(demand_id=demand_id).exclude(address__in=form.cleaned_data['addresses']).delete()
        return HttpResponseRedirect(self.success_url)