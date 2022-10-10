from django.urls import path
from .views import SignUpUserView
from .views import LoginUserView 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('signup/', SignUpUserView.as_view(), name="signup"),
    #path("logout/", LogoutView.as_view(), name="logout")
]