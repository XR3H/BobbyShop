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
    # to login
    if client.is_authenticated and uuid:
        unauth_cart = get_order_or_none(uuid=uuid, status=None)
        if unauth_cart:
            merge_cart(cart, unauth_cart)
    elif uuid:
        cart, _ = Order.objects.get_or_create(uuid=uuid, status=None)

    return cart


def set_cart_quantity(cart_item, quantity):
    cart_item.quantity = quantity
    cart_item.save()
    return cart_item


def get_cart_item(item, order):
    return CartItem.objects.get_or_create(
        order=order,
        item=item,
        defaults={
            'quantity': 0,
            'fixed_price': 0,
            'order': order,
            'item': item
        }
    )

def prepare_cart_full(client, uuid):
    user_id = {'client': client} if client.is_authenticated else {'uuid': uuid}
    return (
        Order.objects.
        prefetch_related('cartitem_set__item').
        select_related('status').
        get_or_create(**user_id, status=None)[0]
    )

def get_order_items(order, item=None):
    if not item:
        return CartItem.objects.filter(
            order=order
        )
    return CartItem.objects.get(
        order=order, item=item
    )
