from django.urls import path, include
from rest_framework import generics
from utils.routers import APIRouter, NestedRouter
from api.users.views import *


# ====== DEV ONLY ======
class _SepView(generics.RetrieveAPIView):
    def get_object(self):
        return self.request.user


_sep_ = path(r"______________________________", _SepView.as_view())
# ====== DEV ONLY ======

router = APIRouter()

router.register(r"workouts", WorkoutViewset)
router.register(r"days", DayViewset)
router.register(r"programs", ProgramViewset)
router.register(r"weeks", WeekViewset)
# router.register(r"exercises", ExerciseViewset)
# router.register("library", LibraryExerciseViewset)

# ========== ========== ==========

nested_router = NestedRouter()

nested_router.register(
    ("workouts", WorkoutViewset),
    ("days", DayViewset),
    # ("exercises", ExerciseViewset),
    # ("sets", SetsViewset),
)
"""
nested_router.register(
    ("programs", ProgramViewset),
    ("weeks", WeekViewset),
    ("exercises", ExerciseViewset),
    ("sets", SetsViewset),
)
"""


customuser_urls = [
    path(
        r"user/", CustomUserViewSet.as_view({"get": "retrieve"}), name="user-readonly"
    ),
    # path(r"user/change/", CustomUserViewSet._as_view({"patch":"partial_update"}), name="user-change"),
    # path(r"user/delete/", CustomUserViewSet._as_view("delete"), name="user-delete"),
    # path(r"user/change-password", CustomUserViewSet.as_detail_view(), name="user-detail"),
]


urlpatterns = customuser_urls + [
    path(r"profile/", ProfileView.as_view(), name="profile-detail"),
    # path("", include(router.urls)),
    _sep_,
    path("", include(nested_router.urls)),
]
