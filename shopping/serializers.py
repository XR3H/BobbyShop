from django.db import transaction
from rest_framework import serializers
from shopping.models import *

class ItemAttributeSerializer(serializers.Serializer):
    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())
    value = serializers.CharField(max_length=80)

class ItemSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=False)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    cost = serializers.FloatField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    attributes = ItemAttributeSerializer(many=True, read_only=False)

    def create(self, validated_data):
        with transaction.atomic():
            item = Item.objects.create(
                title=validated_data.get('title'),
                description=validated_data.get('description'),
                cost=validated_data.get('cost'),
                category=validated_data.get('category')
            )
            for attr in validated_data.get('attributes'):
                ItemAttribute.objects.create(
                    fk_item=item,
                    fk_attribute=attr.get('attribute'),
                    value=attr.get('value')
                )
        return item

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.cost = validated_data.get('cost', instance.cost)
            instance.category = validated_data.get('category', instance.category)
            instance.save()
            # Initial list of attributes transferred in request
            attributes_data = validated_data.get('attributes')
            for attr in ItemAttribute.objects.filter(fk_item=instance):
                # Retrieving database attribute instance from request data
                query_data = next((i for i
                                  in validated_data.get('attributes')
                                  if i.get('attribute').id == attr.fk_attribute.id), None)
                # If present then process else delete
                if query_data is not None:
                    if query_data.get('value') != attr.value:
                        attr.value = query_data.get('value')
                        attr.save()
                    # All already present in database attributes from request processed
                    attributes_data.remove(query_data)
                else:
                    attr.delete()
            # The rest of request attributes (new) have to be created
            for attr in attributes_data:
                ItemAttribute.objects.create(
                    fk_item=instance,
                    fk_attribute=attr.get('attribute'),
                    value=attr.get('value')
                )
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
    attributes = ItemAttributeReadSerializer(many=True, read_only=True)


