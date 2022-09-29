from django.db import models
from core.models import BaseModel, LogicDeletable, Discarder
from collect.models import AddressDemand


class Order(BaseModel, LogicDeletable):

  total_price = models.DecimalField(max_digits=10, decimal_places=4)
  quantity = models.DecimalField(max_digits=10, decimal_places=4)
  address_demand = models.ForeignKey(AddressDemand, on_delete=models.CASCADE)

  def __str__(self):
      return self.quantity