from django.urls import path
from .views import DemandCreateView, DemandListView

urlpatterns = [
    path('demand/create/', DemandCreateView.as_view(), name="create_demand"),
    path('demand/list/', DemandListView.as_view(), name="list_demand"),
]