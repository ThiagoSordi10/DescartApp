from django.urls import path
#from .views import DemandCreateView, DemandListView, DemandUpdateView, DemandAddressesView
from .views import OrderCreateView, OrderListView, OrderUpdateView, DiscardDemandsListView#, OrderAddressesView

urlpatterns = [
    path('order/demand_list/', DiscardDemandsListView.as_view(), name="order_list_demand"),
    path('order/<int:demand_id>/create/', OrderCreateView.as_view(), name="create_order"),
    path('order/list/', OrderListView.as_view(), name="list_order"),   
    path('order/update/<int:pk>', OrderUpdateView.as_view(), name="update_order"),
    #path('order/update/<int:pk>/addresses', OrderAddressesView.as_view(), name="order_address"),
]