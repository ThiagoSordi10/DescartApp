from django.db import models
from core.models import BaseModel, LogicDeletable, Collector


class Demand(BaseModel, LogicDeletable):

  STATUS_CHOICES = (
        ("o", "Open"),
        ("c", "Closed"),
    )

  unit_price = models.DecimalField(max_digits=10, decimal_places=4)
  max_quantity = models.DecimalField(max_digits=10, decimal_places=4)
  min_quantity = models.DecimalField(max_digits=10, decimal_places=4)
  measure = models.CharField(max_length=25)
  item = models.CharField(max_length=255)
  collector = models.ForeignKey(Collector, on_delete=models.CASCADE)
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=False, null=False, default="o")

  def __str__(self):
      return self.item

class Address(BaseModel, LogicDeletable):
    street = models.CharField(max_length=255, default="")
    district = models.CharField(max_length=255, default="")
    number = models.CharField(max_length=8, default="")
    complement = models.CharField(max_length=25, default="")
    zip_code = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)

    def __str__(self):
        return self.street

class AddressDemand(BaseModel, LogicDeletable):

  address = models.ForeignKey(Address, on_delete=models.CASCADE)
  demand = models.ForeignKey(Demand, on_delete=models.CASCADE)

  class Meta:
        unique_together = ['address', 'demand']
