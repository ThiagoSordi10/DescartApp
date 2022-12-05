from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from core.views_mixins import AjaxResponseMixin, JSONResponseMixin
from collect.models import Address, Demand
from collect.forms import AddressForm, AddressUpdateForm
from .base_view import Authorize


class BaseAddress(Authorize):

    context_object_name = "address"
    model = Address
    success_url = reverse_lazy("list_demand")


class BaseDetailAddress(BaseAddress):

    def dispatch(self, request, *args, **kwargs):
        try:
            handler = super(BaseDetailAddress, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object.collector != request.user.collector:
                raise PermissionDenied
            return handler
        except PermissionDenied:
            raise PermissionDenied


@method_decorator(login_required, name='dispatch')
class AdressCreateView(BaseAddress, CreateView):
    
    form_class = AddressForm
    template_name = "address/form.html"
    extra_context = {
        "method": "Create"
    }

    def form_valid(self, form):
        address = form.save(commit = False)
        address.collector = self.request.user.collector
        address.save()
        self.request.session['success'] = "Address saved succesfully"
        return HttpResponseRedirect(reverse_lazy("list_address"))


@method_decorator(login_required, name='dispatch')
class AddressListView(BaseAddress, ListView):

    template_name = "address/list.html"
     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addresses = Address.objects.filter(collector=self.request.user.collector).distinct()

        for address in addresses:
            address.number_demands = Demand.objects.filter(addressdemand__address = address).count()

        paginator = Paginator(addresses, 6)
        page = self.request.GET.get('page')
        addresses_page = paginator.get_page(page)

        context['address_list'] = addresses_page
        context['success'] = self.request.session.pop('success', None) 
        return context


@method_decorator(login_required, name='dispatch')
class AddressUpdateView(BaseDetailAddress, UpdateView):

    form_class = AddressUpdateForm
    template_name = "address/form.html"
    extra_context = {
        "method": "Update"
    }

    def form_valid(self, form):
        address = form.save(commit = True)
        self.request.session['success'] = "Address updated succesfully"
        return HttpResponseRedirect(reverse_lazy("list_address"))


@method_decorator(login_required, name='dispatch')
class AddressDeleteView(JSONResponseMixin, AjaxResponseMixin, BaseDetailAddress, DeleteView):

    def delete_ajax(self, request, *args, **kwargs):
        address = self.get_object()
        address.logic_delete(request.user)
        self.request.session['success'] = "Address deleted succesfully"
        return self.render_json_response({})
