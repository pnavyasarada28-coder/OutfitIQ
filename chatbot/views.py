from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .chatbot_service import get_chatbot_response

class ChatbotAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({'error':'Query is required'},status=status.HTTP_400_BAD_REQUEST)
        response = get_chatbot_response(query)
        return Response({'response': response})
