from django.urls import path
from .views import SignUpUserView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #path('login/', login_view, name="login"),
    path('signup/', SignUpUserView.as_view(), name="signup"),
    #path("logout/", LogoutView.as_view(), name="logout")
]