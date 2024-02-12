from django.db import models
from django.db.models import Model


# Create your models here.

class Item(Model):
    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.title

    title = models.CharField(null=False, blank=False, max_length=80)
    description = models.TextField(null=True, blank=True)
    cost = models.FloatField(null=False, blank=False)

    @property
    def attributes(self):
        return ItemAttribute.objects.filter(fk_item=self)

class Attribute(Model):
    class Meta:
        db_table = 'attribute'

    def __str__(self):
        return self.title

    title = models.CharField(null=False, blank=False, max_length=120)

class ItemAttribute(Model):
    class Meta:
        db_table = 'item_attribute'
        unique_together = ['fk_item', 'fk_attribute']

    fk_item = models.ForeignKey(Item, null=False, on_delete=models.CASCADE)
    fk_attribute = models.ForeignKey(Attribute, null=False, on_delete=models.CASCADE)
    value = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        str_pattern = "{item_id} {item} {attribute_id} {attribute} {value}"
        return str_pattern.format(
            item=self.fk_item,
            item_id=self.fk_item.id,
            value=self.value,
            attribute=self.fk_attribute,
            attribute_id=self.fk_item.id
        )
