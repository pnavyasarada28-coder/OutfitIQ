from django.urls import path
from .views import PlaceOrderAPIView,OrderListAPIView,OrderDetailAPIView

urlpatterns = [
    path('place/',PlaceOrderAPIView.as_view(),name='place-order'),
    path('',OrderListAPIView.as_view(),name='order-list'),
    path('<int:order_id>/',OrderDetailAPIView.as_view(),name='order-detail'),
]