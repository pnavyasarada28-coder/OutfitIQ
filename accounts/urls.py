from django.urls import path
from .views import RegisterAPIView
from .views import ProfileAPIView

urlpatterns = [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('profile/',ProfileAPIView.as_view(),name='profile'),
]