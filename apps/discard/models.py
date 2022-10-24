from django.db import models
from core.models import BaseModel, LogicDeletable, Discarder
from collect.models import AddressDemand


class Order(BaseModel, LogicDeletable):

  STATUS_CHOICES = (
        ("a", "Accepted"),
        ("r", "Refused"),
        ("p", "Pending"),
        ("f", "Finished")
    )

  total_price = models.DecimalField(max_digits=10, decimal_places=4)
  quantity = models.DecimalField(max_digits=10, decimal_places=4)
  address_demand = models.ForeignKey(AddressDemand, on_delete=models.CASCADE)
  discarder = models.ForeignKey(Discarder, on_delete=models.CASCADE)
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=False, null=False, default="p")

  def __str__(self):
      return str(self.id)