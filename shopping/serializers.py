from django.db import transaction
from rest_framework import serializers
from shopping.models import *

class ItemAttributeSerializer(serializers.Serializer):
    # attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())
    attribute = serializers.IntegerField(allow_null=False)
    value = serializers.CharField(max_length=80)

class ItemSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=False)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    cost = serializers.FloatField()
    category = serializers.IntegerField(allow_null=False)
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    attributes = ItemAttributeSerializer(many=True, read_only=False)

    def create(self, validated_data):
        with transaction.atomic():
            item = Item.objects.create(
                title=validated_data.get('title'),
                description=validated_data.get('description'),
                cost=validated_data.get('cost'),
                category_id=validated_data.get('category')
                # category=validated_data.get('category')
            )
            attr_list = []
            for attr in validated_data.get('attributes'):
                attr_list.append(
                    ItemAttribute(
                        fk_item=item,
                        # fk_attribute=attr.get('attribute'),
                        fk_attribute_id=attr.get('attribute'),
                        value=attr.get('value')
                    )
                )
            ItemAttribute.objects.bulk_create(attr_list)
            # for attr in validated_data.get('attributes'):
            #     ItemAttribute.objects.create(
            #         fk_item=item,
            #         fk_attribute=attr.get('attribute'),
            #         value=attr.get('value')
            #         )
        return item

    def update(self, instance, validated_data):
        with transaction.atomic():
            # Cached attribute data list to prevent extra loading of related data
            cached_attrs = []

            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.cost = validated_data.get('cost', instance.cost)
            # instance.category = validated_data.get('category', instance.category)
            instance.category_id = validated_data.get('category', instance.category_id)
            instance.save()
            # Initial list of attributes transferred in request
            attributes_data = validated_data.get('attributes')
            for attr in ItemAttribute.objects.filter(fk_item=instance).select_related('fk_attribute'):
                # Retrieving database attribute instance from request data
                query_data = next((i for i
                                   in validated_data.get('attributes')
                                   # if i.get('attribute').id == attr.fk_attribute.id), None)
                                   if i.get('attribute') == attr.fk_attribute_id), None)
                # If present then process else delete
                if query_data is not None:
                    if query_data.get('value') != attr.value:
                        attr.value = query_data.get('value')
                        attr.save()
                    # All already present in database attributes from request processed
                    attributes_data.remove(query_data)

                    # Present attribute data to be cached
                    cached_attrs.append(attr)
                else:
                    attr.delete()
            # The rest of request attributes (new) have to be created
            for attr in attributes_data:
                attr_data = ItemAttribute.objects.create(
                    fk_item=instance,
                    # fk_attribute=attr.get('attribute'),
                    fk_attribute_id=attr.get('attribute'),
                    value=attr.get('value')
                )
                # New attribute data to be cached
                cached_attrs.append(attr_data)

            instance._prefetched_objects_cache = {'itemattribute_set': cached_attrs}
        return instance


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields='__all__'

class ItemAttributeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAttribute
        exclude = ('id', 'fk_item')

    fk_attribute = AttributeSerializer(many=False, read_only=True)

class ItemReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(allow_null=False)
    description = serializers.CharField(allow_null=True)
    cost = serializers.FloatField()     #digits and null/blank, validator
    itemattribute_set = ItemAttributeReadSerializer(many=True, read_only=True)




