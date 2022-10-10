# Create your views here.
from symbol import import_as_name
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.forms import BaseModelForm
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from typing import Any, Dict
from .forms import SignUpForm
from .forms import LoginForm


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

class LoginUserView(CreateView):
    form_class = LoginForm
    template_name: str = 'user/login.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy(settings.LOGIN_REDIRECT_URL))
        return super(LoginUserView, self).get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Login"""
        user = form.save(commit = False)
        auth_login(self.request, user)

        sucess_url = self.get_success_url()
        return HttpResponseRedirect(sucess_url)