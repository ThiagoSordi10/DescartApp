from django.urls import path
from .views import SignUpUserCollectorView, SignUpUserDiscardView, LoginUserView, LogoutUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('signup_collector/', SignUpUserCollectorView.as_view(), name="signup_collector"),
    path('signup_discarder/', SignUpUserDiscardView.as_view(), name="signup_discarder"),
    path('logout/', LogoutUserView.as_view(), name="logout"),
]