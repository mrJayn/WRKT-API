from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext_lazy as _
from .serializers import RegisterSerializer, ValidateRegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = RegisterSerializer


class ValidateRegisterView(views.APIView):
    permission_classes = ()
    serializer_class = ValidateRegisterSerializer

    def post(self, request, *args, **kwargs):
        print(f"[ValidateRegisterView]  request.data={request.data}")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({}, status=status.HTTP_200_OK)


# class _LogoutView(views.APIView):
#     http_method_names = ["post"]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# class ResetPasswordView(views.APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             recipient = request.data["email"]
#             send_mail(
#                 "Wrkt App - Reset Password",
#                 "Use this link to reset your password.",
#                 "m63jayne@gmail.com",
#                 [recipient],
#                 fail_silently=False,
#             )
#             return Response(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
