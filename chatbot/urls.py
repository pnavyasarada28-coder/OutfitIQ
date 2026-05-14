from django.urls import path
from chatbot.views import (ChatbotAPIView)
urlpatterns = [
    path('',ChatbotAPIView.as_view()),
]