from django.urls import path, include
from utils.routers import CustomRouter, SingleModelRouter
from . import views

router = CustomRouter()
single_model_router = SingleModelRouter()

router.register(r"workouts", views.WorkoutViewset)
router.register(r"programs", views.ProgramViewset)

router.register(r"days", views.DayViewset)
router.register(r"weeks", views.WeekViewset)

router.register(r"exercises", views.ExerciseViewset)

router.register(prefix="library", viewset=views.LibraryExerciseViewset)


urlpatterns = [
    path(r"", views.CustomUserView.as_view(), name="user"),
    path(r"profile/", views.ProfileView.as_view()),
    path(r"profile/<str:detail>/", views.ProfileView.as_view()),
    path(r"", include(router.urls)),
    path(r"", include(single_model_router.urls)),
]
