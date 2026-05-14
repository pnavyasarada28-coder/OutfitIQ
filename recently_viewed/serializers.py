from rest_framework import serializers
from .models import RecentlyViewed
from products.serializers import ProductSerializer

class RecentlyViewedSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = RecentlyViewed
        fields = '__all__'