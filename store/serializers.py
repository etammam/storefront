from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from store.models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products']

    products = serializers.SerializerMethodField(
        method_name='collection_product_count')

    def collection_product_count(self, collection: Collection):
        return collection.products.count()


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )


class ProductDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='price')
    description = serializers.CharField()
    collection = CollectionSerializer()
