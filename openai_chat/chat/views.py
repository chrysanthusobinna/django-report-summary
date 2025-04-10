from django.conf import settings
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .authentication import APIKeyAuthentication
from .serializers import ChatRequestSerializer
import os

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatAPIView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']

            try:
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": settings.OPENAI_SYSTEM_PROMPT},
                        {"role": "user", "content": question}
                    ]
                )

                answer = response.choices[0].message.content.strip()
                return Response({"answer": answer})

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


