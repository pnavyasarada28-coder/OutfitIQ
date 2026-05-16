from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import OrderSerializer


class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'error': 'Cart not found'},status=status.HTTP_404_NOT_FOUND)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        total_price = 0
        # Calculate total price
        for item in cart_items:
            total_price += (item.product.price * item.quantity)
        # Create Order
        order = Order.objects.create(user=request.user,total_price=total_price)
        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Clear cart
        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response({'message': 'Order placed successfully','order': serializer.data},status=status.HTTP_201_CREATED)


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data)
    
class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id,user=request.user).first()
        if not order:
            return Response({'error': 'Order not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
    def delete(self, request, order_id):
        order = Order.objects.filter(id=order_id,user=request.user).first()
        if not order:
            return Response({'error': 'Order not found'},status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_204_NO_CONTENT)