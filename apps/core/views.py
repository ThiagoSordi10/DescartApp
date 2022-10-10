# Create your views here.
from symbol import import_as_name
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import BaseModelForm
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from typing import Any, Dict
from .forms import SignUpForm
from .forms import LoginForm
from .models import Collector, Discarder


class SignUpUserView(CreateView):
    form_class = SignUpForm
    template_name: str = 'user/signup.html'

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
        return HttpResponseRedirect(reverse_lazy('signup'))

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        self.request.session['msg'] = 'Form is invalid'
        return HttpResponseRedirect(reverse_lazy('signup'))

class LoginUserView(LoginView):
    form_class = LoginForm
    template_name: str = 'user/login.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_anonymous:
            try: 
                user = Collector.objects.get(user = request.user)
                return HttpResponseRedirect(reverse_lazy(settings.LOGIN_REDIRECT_URL_COLLECTOR))
            except Collector.DoesNotExist:
                try: 
                    user = Discarder.objects.get(user = request.user)
                    return HttpResponseRedirect(reverse_lazy(settings.LOGIN_REDIRECT_URL_DISCARD))
                except Discarder.DoesNotExist:
                    user = None        
        return super(LoginUserView, self).get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Login"""
        auth_login(self.request, form.get_user())

        return HttpResponseRedirect(reverse_lazy('signup'))

class LogoutUserView(LogoutView):
    next_page: Any = reverse_lazy('login')
