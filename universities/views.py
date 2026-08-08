from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from .models import University
from .serializers import UniversitySerializer
import logging
logger = logging.getLogger(__name__)



# Create your views here.
class UniversityListView(APIView):
    def get(self, request):
        try:
            universities = University.objects.all()
            serializer = UniversitySerializer(
                universities,
                many=True
            )
            return Response ({
                "result" : True, 
                "message": "Universities retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.exception("Unexpected error while retrieving universities: %s",e)
            return Response({
                    "result": False,
                    "error": {
                        "type": "Internal Server Error",
                    },
                    "message": "Something went wrong. Please try again later."
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UniversityDetailView(APIView):
    def get(self, request, pk):
        try: 
            university = University.objects.get(pk=pk)
        except University.DoesNotExist:
            return Response({
                "result": False,
                "error": {
                    "type": "Not Found",
                },
                "message": "University Not Found."
            },status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.exception("Unexpected error while retrieving university %s: %s", pk, e)
            return Response({
                    "result": False,
                    "error": {
                        "type": "Internal Server Error"
                    },
                    "message": "Something went wrong. Please try again later."
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = UniversitySerializer(university)

        return Response({
            "result": True,
            "message": "University retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
