from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from catalog.models import Item

class OrderStatus(models.Model):
    class Meta:
        db_table = 'order_status'

    title = models.CharField(max_length=60, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

class Order(models.Model):
    class Meta:
        db_table = 'order'

    client = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.RESTRICT)
    uuid = models.CharField(null=True, blank=True, max_length=42, validators=[MinLengthValidator(42)])
    status = models.ForeignKey('OrderStatus', null=True, blank=True, on_delete=models.RESTRICT)

    def save(self, *args, **kwargs):
        if (self.uuid is None) == (self.client is None):
            raise ValidationError('Usage of client_fk and uuid is prohibited: these are mutually excluded.')
        super(Order, self).save(*args, **kwargs)


class CartItem(models.Model):
    class Meta:
        db_table = 'cartitem'

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.RESTRICT)
    quantity = models.IntegerField(null=False, blank=False)
    fixed_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.order} {self.item} x{self.quantity} - {self.fixed_price}"