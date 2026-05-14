from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import RecentlyViewed
from .serializers import RecentlyViewedSerializer
from products.models import Product


class AddRecentlyViewedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)
        viewed_product = RecentlyViewed.objects.filter(user=request.user,product=product).first()
        # If already viewed
        if viewed_product:
            viewed_product.save()
        else:
            RecentlyViewed.objects.create(user=request.user,product=product)
        return Response({'message': 'Recently viewed updated'},status=status.HTTP_201_CREATED)
    
class RecentlyViewedListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        viewed_products = RecentlyViewed.objects.filter(user=request.user).order_by('-viewed_at')
        serializer = RecentlyViewedSerializer(viewed_products,many=True)
        return Response(serializer.data)