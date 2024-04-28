from rest_framework.generics import RetrieveAPIView
from api.users.serializers import CustomUserSerializer


class CustomUserView(RetrieveAPIView):
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
