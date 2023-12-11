from rest_framework.generics import ListAPIView
from product.models import Product
from product.serializers import ProductSerializer


class ReportAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

