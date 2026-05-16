from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer

# Central mapping for style composition
COMPLEMENTARY_MAP = {
    'kurti': ['legging', 'leggings', 'handbag', 'earring', 'sandal', 'watch', 'dupatta', 'heels', 'bracelet', 'accessory'],
    'hoodie': ['sneaker', 'cargo', 'watch', 'cap', 'jogger', 'jeans', 't-shirt'],
    'shirt': ['trouser', 'loafer', 'belt', 'watch', 'jeans', 'chinos', 'shoe'],
    'sneaker': ['jogger', 'hoodie', 'cap', 't-shirt', 'short', 'jeans'],
    'dress': ['heels', 'handbag', 'earring', 'necklace', 'bracelet', 'jacket'],
    't-shirt': ['jeans', 'short', 'sneaker', 'cap', 'jacket', 'watch'],
    'jeans': ['t-shirt', 'shirt', 'sneaker', 'shoe', 'belt', 'jacket', 'hoodie']
}

class SimilarProductsAPIView(APIView):
    # Removed IsAuthenticated to allow anonymous users
    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'}, status=404)
            
        # Try finding same category and same gender
        similar_products = Product.objects.filter(
            category=product.category,
            gender=product.gender
        ).exclude(id=product.id)
        
        recs = list(similar_products[:8])
        
        # Fallback to same gender if not enough
        if len(recs) < 4:
            additional = Product.objects.filter(gender=product.gender).exclude(
                id__in=[r.id for r in recs] + [product.id]
            )[:8 - len(recs)]
            recs.extend(list(additional))
            
        # Ultimate fallback if still empty
        if len(recs) == 0:
            recs = list(Product.objects.exclude(id=product.id)[:8])
        
        serializer = ProductSerializer(recs, many=True)
        return Response(serializer.data)


class CompleteTheLookAPIView(APIView):
    # Removed IsAuthenticated to allow anonymous users
    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'}, status=404)
            
        current_cat_name = product.category.name.lower() if product.category else ''
        
        # Look up complementary categories
        comp_categories = []
        for key, value in COMPLEMENTARY_MAP.items():
            if key in current_cat_name:
                comp_categories.extend(value)
                break
                
        # Base query: matching gender and exclude current category explicitly
        recommendations = Product.objects.filter(gender=product.gender)
        if product.category:
            recommendations = recommendations.exclude(category=product.category)
            
        recs = []
        
        if comp_categories:
            from django.db.models import Q
            q_objects = Q()
            for cat in comp_categories:
                q_objects |= Q(category__name__icontains=cat)
                
            filtered_recs = recommendations.filter(q_objects).distinct()[:6]
            recs = list(filtered_recs)
            
            # Fallback within different categories if mapping yielded few results
            if len(recs) < 4:
                additional_recs = recommendations.exclude(id__in=[r.id for r in recs])[:6 - len(recs)]
                recs.extend(list(additional_recs))
        else:
            recs = list(recommendations[:6])
            
        # Broad Fallback if we STILL don't have enough (e.g. dataset lacks variety)
        # fallback to broader gender-compatible products
        if len(recs) < 4:
            broad_fallback = Product.objects.filter(gender=product.gender).exclude(
                id__in=[r.id for r in recs] + [product.id]
            )[:6 - len(recs)]
            recs.extend(list(broad_fallback))
            
        # Ultimate safety net, any product
        if len(recs) == 0:
            recs = list(Product.objects.exclude(id=product.id)[:6])
            
        serializer = ProductSerializer(recs, many=True)
        return Response({
            'current_product': ProductSerializer(product).data,
            'complete_the_look': serializer.data
        })
