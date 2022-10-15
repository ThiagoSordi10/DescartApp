from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Demand

class DemandForm(forms.ModelForm):
    
    class Meta:
        model = Demand