from django.urls import path
from .views import DemandCreateView

urlpatterns = [
    path('demand/create/', LoginUserView.as_view(), name="create_demand"),
]