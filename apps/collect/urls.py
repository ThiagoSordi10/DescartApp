from django.urls import path
from .views import DemandCreateView, DemandDeleteView, DemandListView, DemandUpdateView, DemandAddressesView, DemandUpdateStatusView, AdressCreateView, CollectOrdersListView

urlpatterns = [
    path('demand/create/', DemandCreateView.as_view(), name="create_demand"),
    path('demand/list/', DemandListView.as_view(), name="list_demand"),
    path('demand/update/<int:pk>', DemandUpdateView.as_view(), name="update_demand"),
    path('demand/delete/<int:pk>', DemandDeleteView.as_view(), name="delete_demand"),
    path('demand/update/<int:pk>/status', DemandUpdateStatusView.as_view(), name="update_demand_status"),
    path('demand/update/<int:pk>/addresses', DemandAddressesView.as_view(), name="demand_address"),
    path('demand/<int:pk>/order_list', CollectOrdersListView.as_view(), name="demand_list_orders"),
    path('address/create/', AdressCreateView.as_view(), name="create_adress"),
]