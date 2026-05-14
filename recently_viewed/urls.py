from django.urls import path
from .views import AddRecentlyViewedAPIView,RecentlyViewedListAPIView


urlpatterns = [
    path('add/',AddRecentlyViewedAPIView.as_view(),name='add-recently-viewed'),
    path('',RecentlyViewedListAPIView.as_view(),name='recently-viewed-list'),
]