from rest_framework.serializers import ModelSerializer
from api.users.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        # [
        #     "basic_editor",
        #     "prefers_metric",
        #     "notifs",
        #     "day_one_wkday",
        #     "time_offset",
        #     "units",
        # ]
