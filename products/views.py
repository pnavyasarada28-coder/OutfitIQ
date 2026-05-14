from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import render

def home(request):
    return render(request,'index.html')

def login_page(request):
    return render(request,'login.html')

def cart_page(request):
    return render(request,'cart.html')

def product_detail_page(request,product_id):
    context = {"product_id": product_id}
    return render(request,'product_detail.html',context)

class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        search_query = request.query_params.get('search', None)
        if search_query:
            products = products.filter(title__icontains=search_query)
        page = int(request.query_params.get('page', 1))
        page_size = 8
        start = (page - 1) * page_size
        end = start + page_size
        paginated_products = products[start:end]
        serializer = ProductSerializer(paginated_products,many=True)
        return Response({'count': products.count(),'page': page,'results': serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'message': 'Product deleted successfully'},status=status.HTTP_204_NO_CONTENT)
