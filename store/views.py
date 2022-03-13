from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductDetailsSerializer, ProductSerializer


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        deserializer = ProductSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        print(deserializer.data)
        return Response('Ok')


class ProductDetails(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        deserailzer = ProductDetailsSerializer(product, data=request.data)
        deserailzer.is_valid(raise_exception=True)
        deserailzer.save()
        return Response(deserailzer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderItems.count() > 0:
            return Response({'error': 'can not delete this product becouse there are assoicated orders'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        collection_deserializer = CollectionSerializer(collection)
        return Response(collection_deserializer.data)

    def put(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        collection_deserializer = CollectionSerializer(
            collection, data=request.data)
        collection_deserializer.is_valid(raise_exception=True)
        collection_deserializer.save()
        return Response(collection_deserializer.data)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(data={'error': 'cant delete the collection becouse it has assocatied products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(
            collections, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        deserializer = CollectionSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        print(deserializer.data)
        return Response('Ok')
