from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, UpdateView
from django.http import HttpResponseRedirect
from django.db.models import Q

from django.core.paginator import Paginator

from collect.models import Demand, Address, AddressDemand
from .models import Order
from .forms import OrderForm, OrderUpdateForm, OrderAddressesForm
from core.models import Discarder
from core.views_mixins import AjaxResponseMixin, JsonRequestResponseMixin
from collect.views import Authorize

class BaseOrder():

    context_object_name = "order"
    model = Order
    success_url = reverse_lazy("list_order")

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        try: 
            user = Discarder.objects.get(user = self.request.user)
            return handler
        except Discarder.DoesNotExist:
            raise PermissionDenied


class BaseDetailCollectorOrder(Authorize):

    model = Order

    def dispatch(self, request, *args, **kwargs):
        try:
            handler = super(BaseDetailCollectorOrder, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object.address_demand.demand.collector != request.user.collector:
                raise PermissionDenied
            return handler
        except PermissionDenied:
            raise PermissionDenied

class BaseDetailOrder(BaseOrder):

    def dispatch(self, request, *args, **kwargs):
        try:
            super(BaseDetailOrder, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object.discarder != request.user.discarder:
                raise PermissionDenied
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except PermissionDenied:
            raise PermissionDenied

@method_decorator(login_required, name='dispatch')
class OrderCreateView(BaseOrder, CreateView):

    form_class = OrderForm
    template_name = "order/form.html"
    extra_context = {
        "method": "Create"
    }

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        kwargs['city'] = self.request.GET.get('city')
        return kwargs

    def form_valid(self, form):
        order = form.save(commit = False)
        order.discarder = self.request.user.discarder
        order.total_price = order.quantity * order.address_demand.demand.unit_price
        order.save()
        return HttpResponseRedirect(self.success_url)

@method_decorator(login_required, name='dispatch')
class OrderListView(BaseOrder, ListView):

    template_name = "order/list.html"
     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(discarder=self.request.user.discarder).distinct()

        paginator = Paginator(orders, 6)
        page = self.request.GET.get('page')
        orders_page = paginator.get_page(page)

        context['order_list'] = orders_page
        return context


@method_decorator(login_required, name='dispatch')
class DiscardDemandsListView(BaseOrder, ListView):

    model = Demand
    template_name = "order/demand_list.html"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city', None)
        filter_city = Q(addressdemand__address__city__icontains=city.lower()) if city else Q()
        demands = Demand.objects.filter(filter_city, status='o').distinct()

        paginator = Paginator(demands, 6)
        page = self.request.GET.get('page')
        demands_page = paginator.get_page(page)

        context['demands_list'] = demands_page
        context['city'] = city
        return context


@method_decorator(login_required, name='dispatch')
class OrderUpdateStatusView(JsonRequestResponseMixin, AjaxResponseMixin, BaseDetailCollectorOrder,  UpdateView):

    require_json = True

    def put_ajax(self, request, *args, **kwargs):
        try:
            status = self.request_json[u"status"]
            if status in [c[0] for c in Order.status.field.choices]:
                order = self.get_object()
                order.status = status
                order.save()
                return self.render_json_response({})
            error_dict = {"message": "status not valid"}
            return self.render_bad_request_response(error_dict)
        except KeyError:
            error_dict = {"message": "your order must include a status"}
            return self.render_bad_request_response(error_dict)
