from django.urls import path
from .views import DemandCreateView, DemandListView, DemandUpdateView, DemandAddressesView

urlpatterns = [
    path('demand/create/', DemandCreateView.as_view(), name="create_demand"),
    path('demand/list/', DemandListView.as_view(), name="list_demand"),
    path('demand/update/<int:pk>', DemandUpdateView.as_view(), name="update_demand"),
    path('demand/update/<int:pk>/addresses', DemandAddressesView.as_view(), name="demand_address"),
]