# Create your views here.
from symbol import import_as_name
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import BaseModelForm
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from typing import Any, Dict
from .forms import SignUpForm
from .forms import LoginForm
from .models import Collector, Discarder

def user_type_redirect(request: HttpRequest) -> HttpResponse:
    try: 
        user = Collector.objects.get(user = request.user)
        return HttpResponseRedirect(reverse_lazy(settings.LOGIN_REDIRECT_URL_COLLECTOR))
    except Collector.DoesNotExist:
        try: 
            user = Discarder.objects.get(user = request.user)
            return HttpResponseRedirect(reverse_lazy(settings.LOGIN_REDIRECT_URL_DISCARD))
        except Discarder.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('login'))

class UserAuthenticatedView():

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_anonymous:
            return user_type_redirect(request)      
        return super(UserAuthenticatedView, self).get(request, *args, **kwargs)

class SignUpUserView(UserAuthenticatedView, CreateView):
    form_class = SignUpForm
    template_name: str = 'user/signup.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super(SignUpUserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['msg'] = self.request.session.pop('msg', None)
        context['success'] = self.request.session.pop('success', False)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save(commit = False)
        names = form.cleaned_data.get("name").split()
        user.first_name = names[0]
        user.last_name = " ".join(names[1:])
        user.is_active = True
        user.save()

        self.request.session['success'] = True
        self.request.session['msg'] = 'User created - please <a href="/login">login</a>.'
        return user

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        context = super().get_context_data()
        context['msg'] = 'Form is invalid'
        context['form'] = form
        context['form']._errors = form.errors
        return self.render_to_response(context)

class SignUpUserCollectorView(SignUpUserView):


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(SignUpUserCollectorView, self).get_context_data(**kwargs)
        context['user_type'] = 'Collector'
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = super(SignUpUserCollectorView, self).form_valid(form)
        c = Collector(user = user)
        c.save()
        return HttpResponseRedirect(reverse_lazy('signup_collector'))

    def form_invalid(self, form:BaseModelForm) -> HttpResponse:
        return super(SignUpUserCollectorView, self).form_invalid(form)
        

class SignUpUserDiscardView(SignUpUserView):

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(SignUpUserDiscardView, self).get_context_data(**kwargs)
        context['user_type'] = 'Discarder'
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = super(SignUpUserDiscardView, self).form_valid(form)
        d = Discarder(user = user)
        d.save()
        return HttpResponseRedirect(reverse_lazy('signup_discarder'))

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super(SignUpUserDiscardView, self).form_invalid(form)


class LoginUserView(UserAuthenticatedView, LoginView):
    form_class = LoginForm
    template_name: str = 'user/login.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super(LoginUserView, self).get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Login"""
        auth_login(self.request, form.get_user())
        next_url = self.request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
        return user_type_redirect(self.request)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        context = super().get_context_data()
        context['msg'] = 'Form is invalid'
        context['form'] = form
        context['form']._errors = form.non_field_errors()
        return self.render_to_response(context)
    

class LogoutUserView(LogoutView):
    next_page: Any = reverse_lazy('login')
