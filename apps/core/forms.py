from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

    def clean_password(self):
        password = self.cleaned_data['password']
        return password


class SignUpForm(UserCreationForm):

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        ))
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = get_user_model()
        fields = ('name','phone', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        users = get_user_model().objects.filter(email__iexact=email)
        if users:
            raise forms.ValidationError("E-mail already exists.")
        return email.lower()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        users = get_user_model().objects.filter(phone__iexact=phone)
        if users:
            raise forms.ValidationError("Phone already exists.")
        return phone
