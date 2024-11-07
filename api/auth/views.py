from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ValidateUserSerializer


class ValidateUserView(APIView):
    """
    View to validate unique fields for a user.
    """

    permission_classes = []
    serializer_class = ValidateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({}, status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    """
    View to create a user.
    """

    permission_classes = []
    serializer_class = RegisterSerializer
