from cart.models import Order, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Subquery, OuterRef, Max, Min


def get_order_or_none(**kwargs):
    instance = None
    try:
        instance = Order.objects.get(**kwargs)
    except ObjectDoesNotExist:
        pass
    return instance


def merge_cart(master, merged):
    # "Privatize" marged-specific item positions
    master_subq = CartItem.objects.filter(order=master).values('item_id')
    CartItem.objects.filter(order=merged).exclude(item_id__in=Subquery(master_subq)).update(
        order=master
    )

    # "Merge" quantity of shared positions into one composal record
    master_subq = CartItem.objects.filter(
        order=master, item_id=OuterRef('item_id')
    ).values('quantity')
    CartItem.objects.filter(order=merged).update(
        quantity=F('quantity') + Subquery(master_subq), order=master
    )

    # "Utilize" non-composal record of any item
    max_quantity_subq = CartItem.objects.filter(
        order=master, item_id=OuterRef('item_id')
    ).values('item_id').annotate(
        max_quantity=Max('quantity')
    ).values('max_quantity')[:1]
    CartItem.objects.filter(order=master).exclude(quantity__in=Subquery(max_quantity_subq)).delete()

    merged.delete()


def prepare_cart_order(client, uuid):
    cart = None

    if client.is_authenticated:
        cart, _ = Order.objects.get_or_create(client=client, status=None)
    if client.is_authenticated and uuid:
        unauth_cart = get_order_or_none(uuid=uuid, status=None)
        if unauth_cart:
            merge_cart(cart, unauth_cart)
    elif uuid:
        cart, _ = Order.objects.get_or_create(uuid=uuid, status=None)

    return cart


def add_to_cart(order, item, quantity):
    cart_item, _ = CartItem.objects.get_or_create(
        order=order,
        item=item,
        defaults={
            'quantity': 0,
            'fixed_price': 0,
            'order': order,
            'item': item
        }
    )
    cart_item.quantity += quantity
    cart_item.save()
    return cart_item
