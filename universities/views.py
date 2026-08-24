from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from .models import University, Program
from .serializers import ProgramSerializer, UniversityDetailSerializer, UniversitySerializer
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

    def post(self, request):
        try:
            serializer = UniversitySerializer(data=request.data)
            if serializer.is_valid():
                university = serializer.save()
                return Response({
                    "result": True,
                    "message": "University created successfully.",
                    "data": UniversitySerializer(university).data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "result": False,
                "message": "Invalid University data.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error while creating university: %s", e)
            return Response({
                "result": False,
                "message" : "An unexpected error occured",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

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
        serializer = UniversityDetailSerializer(university)
        return Response({
            "result": True,
            "message": "University retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            university = University.objects.get(pk=pk)
        except University.DoesNotExist:
            return Response({
                "result": False,
                "message": "University Not Found."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.exception("Unexpected error while retrieving university %s: %s", pk, e)
            return Response({
                "result": False,
                "message": "Something went wrong."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = UniversitySerializer(
            university, 
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            university = serializer.save()
            return Response({
                "result": True,
                "message": "University updated successfully.",
                "data": UniversityDetailSerializer(university).data
            }, status=status.HTTP_200_OK)
        return Response({
            "result": False,
            "message": "Invalid University data.",
            "data": serializer.errors
        }, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            university = University.objects.get(pk=pk)
            university.delete()
            return Response({
                "result": True,
                "message": "University deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except University.DoesNotExist:
            return Response({
                "result": False,
                "message": "University Not Found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error while deleting university %s: %s", pk, e)
            return Response({
                "result": False,
                "message": "Something went wrong."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ProgramListView(APIView):
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
        programs = Program.objects.filter(university=university)       
        serializer = ProgramSerializer(programs, many=True)
        return Response({
            "result": True,
            "message": "Programs retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, pk):
        try:
            university = University.objects.get(pk=pk)
        except University.DoesNotExist:
            return Response({
                "result" : False,
                "message": "University Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error while creating university: %s", e)
            return Response({
                "result": False,
                "message" : "An unexpected error occured",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            program = serializer.save(university=university)
            return Response({
                "result": True,
                "message": "Program created successfully.",
                "data": ProgramSerializer(program).data
            })
        
        return Response({
            "result": False,
            "message": "Invalid Program data.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)