from utils.serializers import UserModelSerializer
from api.users.models import Profile


class ProfileSerializer(UserModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "id",
            "notifications",
            "day_one_wkday",
            "units",
            "theme",
            "locale",
        ]
