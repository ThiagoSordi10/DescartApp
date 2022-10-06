# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.forms import BaseModelForm
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from typing import Any, Dict
from .forms import SignUpForm


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
