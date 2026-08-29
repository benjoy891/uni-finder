from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
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


class UserLoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            if not username or not password:
                return Response({
                    "result": True,
                    "message": "Username and password are required",
                }, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({
                    "result": False,
                    "message": "Invalid username or password",
                }, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({
                    "result": True,
                    "message": "Login successful",
                    "data": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }
                }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "result": False,
                "message": "An unexpected error occurred",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)