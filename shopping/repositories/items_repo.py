from typing import Optional

from django.db.models import QuerySet

from shopping.models import Item


def all_items_with_attributes() -> Optional[ QuerySet[Item] ]:
    return (
        Item.objects.
        prefetch_related('itemattribute_set__fk_attribute').
        select_related('category').
        all()
    )


def get_item_with_attributes(id: int) -> Optional[Item]:
    return (
        Item.objects.
        prefetch_related('itemattribute_set__fk_attribute').
        select_related('category').
        get(id=id)
    )

def get_item(id: int) -> Optional[Item]:
    return Item.objects.get(id=id)

