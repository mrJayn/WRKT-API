from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from utils.mixins import PartialUpdateModelMixin
from api.users.serializers import ProfileSerializer


class ProfileView(PartialUpdateModelMixin, RetrieveAPIView):
    serializer_class = ProfileSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        profile = self.request.user.profile
        detail = kwargs.get("detail", None)
        if detail:
            return Response({detail: getattr(profile, detail, None)})
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
