from rest_framework.generics import RetrieveUpdateAPIView
from api.users.models import Profile
from api.users.serializers import ProfileSerializer


class ProfileView(RetrieveUpdateAPIView):
    """
    View for retrieving, updating a `Profile` model instance.
    """

    http_method_names = ["get", "patch"]
    model = Profile
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
