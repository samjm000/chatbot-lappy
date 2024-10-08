from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from haystack_config import pipeline

def index(request):
    return HttpResponse("Welcome to the AI Chatbot!")

class ChatbotAPIView(APIView):
    def post(self, request):
        question = request.data.get("question")
        result = pipeline.run(query=question)
        return Response(result)
