from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from config.paginator import CustomPagination
from users.permissions import IsStaffUser
from .models import University, Program
from .serializers import ProgramSerializer, UniversityDetailSerializer, UniversitySerializer
import logging
logger = logging.getLogger(__name__)
from rest_framework.exceptions import NotFound



class UniversityView(APIView):
    permission_classes = [IsStaffUser]
    pagination_class = CustomPagination

    def get(self, request):
        try:
            universities = University.objects.all().order_by("id")
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(universities, request, view=self)
            serializer = UniversitySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        except NotFound as e:
            return Response({
                "result": False,
                "error": {"type": "Not Found"},
                "message": str(e.detail),
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception("Unexpected error while retrieving universities: %s", e)
            return Response({
                "result": False,
                "error": {"type": "Internal Server Error"},
                "message": "Something went wrong. Please try again later.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                "message": "An unexpected error occured",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk=None):
        try:
            university = University.objects.get(pk=pk)
        except University.DoesNotExist:
            return Response({
                "result": False,
                "message": "University Not Found."
            }, status=status.HTTP_404_NOT_FOUND)

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

    def delete(self, request, pk=None):
        try:
            university = University.objects.get(pk=pk)
            university.delete()
            return Response({
                "result": True,
                "message": "University deleted successfully."
            }, status=status.HTTP_200_OK)
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


class ProgramView(APIView):
    permission_classes = [IsStaffUser]
    pagination_class = CustomPagination

    def get(self, request, university_pk=None):
        try:
            university = University.objects.get(pk=university_pk)
            programs = Program.objects.filter(university=university).order_by("id")
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(programs, request, view=self)
            serializer = ProgramSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        except University.DoesNotExist:
            return Response({
                "result": False,
                "error": {"type": "Not Found"},
                "message": "University Not Found."
            }, status=status.HTTP_404_NOT_FOUND)

        except NotFound as e:
            return Response({
                "result": False,
                "error": {"type": "Not Found"},
                "message": str(e.detail),
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception("Unexpected error while retrieving programs for university %s: %s", university_pk, e)
            return Response({
                "result": False,
                "error": {"type": "Internal Server Error"},
                "message": "Something went wrong. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, university_pk=None):
        try:
            university = University.objects.get(pk=university_pk)
        except University.DoesNotExist:
            return Response({
                "result": False,
                "message": "University Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error while creating program: %s", e)
            return Response({
                "result": False,
                "message": "An unexpected error occured",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            program = serializer.save(university=university)
            return Response({
                "result": True,
                "message": "Program created successfully.",
                "data": ProgramSerializer(program).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "result": False,
            "message": "Invalid Program data.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            program = Program.objects.get(pk=pk)
        except Program.DoesNotExist:
            return Response({
                "result": False,
                "message": "Program Not Found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error while retrieving program %s: %s", pk, e)
            return Response({
                "result": False,
                "message": "Something went wrong."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ProgramSerializer(
            program,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            program = serializer.save()
            return Response({
                "result": True,
                "message": "Program updated successfully.",
                "data": ProgramSerializer(program).data
            }, status=status.HTTP_200_OK)
        return Response({
            "result": False,
            "message": "Invalid Program data.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            program = Program.objects.get(pk=pk)
            program.delete()
            return Response({
                "result": True,
                "message": "Program deleted successfully."
            }, status=status.HTTP_200_OK)
        except Program.DoesNotExist:
            return Response({
                "result": False,
                "message": "Program Not Found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error while deleting program %s: %s", pk, e)
            return Response({
                "result": False,
                "message": "Something went wrong."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)