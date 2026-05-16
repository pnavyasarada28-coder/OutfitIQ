from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST,HTTP_201_CREATED,HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=HTTP_400_BAD_REQUEST)
        
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'},status=HTTP_404_NOT_FOUND)
        
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)

        cart_item = CartItem.objects.filter(cart=cart,product=product).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart,product=product,quantity=1)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=HTTP_201_CREATED if cart_item else HTTP_200_OK)

    def delete(self, request):
        product_id = request.data.get('product_id') or request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=HTTP_400_BAD_REQUEST)
            
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=HTTP_404_NOT_FOUND)
            
        cart_item = CartItem.objects.filter(cart=cart,product_id=product_id).first()
        if not cart_item:
            return Response({'error': 'Item not in cart'},status=HTTP_404_NOT_FOUND)
        
        cart_item.delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=HTTP_200_OK)