from django.urls import path
from .views import SimilarProductsAPIView,CompleteTheLookAPIView

urlpatterns = [
    path('similar/<int:product_id>/',SimilarProductsAPIView.as_view(),name='similar-products'),
    path('complete-look/<int:product_id>/',CompleteTheLookAPIView.as_view(),name='complete-look'),
]