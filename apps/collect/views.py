from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from core.views_mixins import AjaxResponseMixin, JsonRequestResponseMixin, JSONResponseMixin
# from braces.views import AjaxResponseMixin, JsonRequestResponseMixin
from .models import Demand, Address, AddressDemand
from .forms import AdressForm, DemandForm, DemandUpdateForm, DemandAddressesForm
from core.models import Collector
from discard.models import Order

class Authorize():

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        try: 
            user = Collector.objects.get(user = self.request.user)
            return handler
        except Collector.DoesNotExist:
            raise PermissionDenied

class BaseDemand(Authorize):

    context_object_name = "demand"
    model = Demand
    success_url = reverse_lazy("list_demand")

    
class BaseAddress(Authorize):

    context_object_name = "address"
    model = Address
    success_url = reverse_lazy("list_demand")


class BaseDetailDemand(BaseDemand):

    def dispatch(self, request, *args, **kwargs):
        try:
            handler = super(BaseDetailDemand, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object.collector != request.user.collector:
                raise PermissionDenied
            return handler
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

        for demand in demands:
            demand.pending_orders = Order.objects.filter(address_demand__demand = demand, status='p').count()
            demand.value_bought = Order.objects.filter(address_demand__demand = demand, status='f').aggregate(Sum('total_price'))['total_price__sum']

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

@method_decorator(login_required, name='dispatch')
class DemandDeleteView(JSONResponseMixin, AjaxResponseMixin, BaseDetailDemand, DeleteView):

    def delete_ajax(self, request, *args, **kwargs):
        demand = self.get_object()
        demand.logic_delete(request.user)
        return self.render_json_response({})

@method_decorator(login_required, name='dispatch')
class DemandUpdateStatusView(JsonRequestResponseMixin, AjaxResponseMixin, BaseDetailDemand,  UpdateView):

    require_json = True

    def put_ajax(self, request, *args, **kwargs):
        try:
            status = self.request_json[u"status"]
        except KeyError:
            error_dict = {"message": "your order must include a status"}
            return self.render_bad_request_response(error_dict)
        demand = self.get_object()
        demand.status = status
        demand.save()
        return self.render_json_response({})


@method_decorator(login_required, name='dispatch')
class DemandAddressesView(BaseDetailDemand, UpdateView):

    form_class = DemandAddressesForm
    template_name = "demand/demand_address.html"

    def get_form_kwargs(self):
        kwargs = super(DemandAddressesView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs.update(self.kwargs)
        return kwargs

    def form_valid(self, form):
        demand = self.get_object()
        for address in form.cleaned_data['addresses']:
            AddressDemand.objects.get_or_create(address=address, demand=demand)
        AddressDemand.objects.filter(demand=demand).exclude(address__in=form.cleaned_data['addresses']).delete()
        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class AdressCreateView(BaseAddress, CreateView):
    
    form_class = AdressForm
    template_name = "address/new.html"

    def form_valid(self, form):
        adress = form.save(commit = False)
        adress.collector = self.request.user.collector
        adress.save()
        return HttpResponseRedirect(reverse_lazy("list_demand"))

@method_decorator(login_required, name='dispatch')
class CollectOrdersListView(BaseDetailDemand, DetailView):

    model = Demand
    template_name = "demand/order_list.html"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status', 'p')
        filter_status = Q(status=status)
        demand = self.get_object()
        orders = Order.objects.filter(filter_status, address_demand__demand=demand).distinct()

        paginator = Paginator(orders, 6)
        page = self.request.GET.get('page')
        orders_page = paginator.get_page(page)

        context['orders_list'] = orders_page
        context['status'] = status
        return context
