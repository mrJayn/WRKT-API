from .user import UserAdmin
from .profile import ProfileAdmin
from .workouts import WorkoutAdmin, DayAdmin
from .programs import ProgramAdmin

from . import exercises

USER_MODELS_ORDER = [
    "CustomUser",
    "Profile",
    "Workout",
    "Day",
    "Program",
    "Week",
    "Exercise",
]
