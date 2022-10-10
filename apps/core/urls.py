from django.urls import path
from .views import SignUpUserView, LoginUserView, LogoutUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('signup/', SignUpUserView.as_view(), name="signup"),
    path('logout/', LogoutUserView.as_view(), name="logout"),
]