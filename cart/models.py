from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from catalog.models import Item

class Order(models.Model):
    class Meta:
        db_table = 'order'

    client = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.RESTRICT)
    uuid = models.IntegerField(null=True, blank=True)


    def clean(self):
        if (self.uuid is None) == (self.client is None):
            raise ValidationError('Usage of client_fk and uuid is prohibited: these are mutually excluded.')


class CartItem(models.Model):
    class Meta:
        db_table = 'cartitem'

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.RESTRICT)
    quantity = models.IntegerField(null=False, blank=False)
    fixed_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.order} {self.item} x{self.quantity} - {self.fixed_price}"