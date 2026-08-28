from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserResgistrationSerializer

# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserResgistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    "result": True,
                    "message": "User registered successfully",
                    "data": {
                        "username": user.username,
                        "email": user.email,
                    }
                }, status=status.HTTP_201_CREATED)
            return Response({
                "result": False,
                "message": "Invalid registration data",
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "result": False,
                "message": "An unexpected error occurred",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
