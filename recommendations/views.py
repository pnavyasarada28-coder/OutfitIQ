from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer

class SimilarProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'},status=404)
        similar_products = Product.objects.filter(style_type=product.style_type,gender=product.gender).exclude(id=product.id)[:8]
        serializer = ProductSerializer(similar_products,many=True)
        return Response(serializer.data)


class CompleteTheLookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'},status=404)
        recommendations = Product.objects.filter(style_type=product.style_type).exclude(category=product.category).exclude(id=product.id)[:6]
        serializer = ProductSerializer(recommendations,many=True)
        return Response({'current_product': ProductSerializer(product).data,'complete_the_look': serializer.data})
    
