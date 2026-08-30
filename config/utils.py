from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response({
                "result": False,
                "message": "Authentication credentials were not provided.",
            }, status=status.HTTP_401_UNAUTHORIZED)

        if response.status_code == status.HTTP_403_FORBIDDEN:
            return Response({
                "result": False,
                "message": "You do not have permission to perform this action",
            }, status=status.HTTP_403_FORBIDDEN)

    return response