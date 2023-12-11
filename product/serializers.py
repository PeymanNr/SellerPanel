from rest_framework import serializers
from product.models import Product, Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    price = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'created_time', 'description', 'update_time', 'price')