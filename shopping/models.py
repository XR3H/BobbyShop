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