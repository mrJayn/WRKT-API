_BODYPART_CHOICES = [
    "chest",
    "back",
    "arms",
    "shoulders",
    "legs",
    "core",
    "",
]
_EQUIPMENT_CHOICES = [
    "barbell",
    "ez_bar",
    "dumbell",
    "cable",
    "sm",
    "machine",
    "bodyweight",
    "freeweight",
    "bands",
    "",
]


PUBLIC_ROUTES = {
    "register": {
        "url": "register/",
        "detail": None,
        "methods": ["post"],
        "body": {
            "post": {
                "email": "<String>",
                "username": "<String>",
                "password": "<String>",
                "submitted": "<Boolean>",
            },
            "patch": None,
        },
        "params": None,
    },
    "login": {
        "url": "login/",
        "detail": None,
        "methods": ["post"],
        "body": {
            "post": {"email": "<String>", "password": "<String>"},
            "patch": None,
        },
        "params": None,
    },
    "logout": {
        "url": "logout/",
        "detail": None,
        "methods": ["post"],
        "body": {
            "post": {"refresh": "<String>"},
            "patch": None,
        },
        "params": None,
    },
    "refresh": {
        "url": "refresh/",
        "detail": None,
        "methods": ["post"],
        "body": {
            "post": {"refresh": "<String>"},
            "patch": None,
        },
        "params": None,
    },
    "delete": {
        "url": "delete/",
        "detail": None,
        "methods": ["post"],
        "body": {
            "post": None,
            "patch": None,
        },
        "params": None,
    },
    "routes": {
        "url": "/routes/",
        "detail": "<name>",
        "methods": ["get"],
        "body": None,
        "params": None,
    },
}

ROUTES = {
    "user": {
        "url": "/user/",
        "detail": None,
        "methods": ["get"],
        "body": None,
        "params": None,
    },
    "profile": {
        "url": "user/profile/",
        "detail": "<detail>/",
        "methods": ["get", "patch"],
        "body": {
            "post": None,
            "patch": {
                "basic_editor": "<Boolean>",
                "prefers_metric": "<Boolean>",
                "notifs": "<Boolean>",
                "day_one_wkday": "<Number>",
            },
        },
        "params": None,
    },
    "workout": {
        "url": "/user/workouts/",
        "detail": "<wkt_order>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {"name": "<String>"},
            "patch": {"name": "<String>", "order": "<Number>", "active": "<Boolean>"},
        },
        "params": {"active_pk"},
    },
    "day": {
        "url": "/user/workouts/<workout>/days/",
        "detail": "<day>/",
        "methods": ["get", "patch"],
        "body": {
            "post": None,
            "patch": {"name": "<String>"},
        },
        "params": None,
    },
    "wkt_exercise": {
        "url": "/user/workouts/<wkt_order>/days/<day>/exercises/",
        "detail": "<exercise>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {"name": "<String>", "order": "<String>"},
            "patch": {"name": "<String>"},
        },
        "params": None,
    },
    "wkt_secondary": {
        "url": "/user/workouts/<wkt_order>/days/<day>/exercises/<exercise>/secondary/",
        "detail": "add/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {
                "name": "<String>",
                "sets": "<String>",
                "reps": "<String>",
                "weight": "<String>",
            },
            "patch": {"name": "<String>"},
        },
        "params": None,
    },
    "wkt_set": {
        "url": "/user/workouts/<wkt_order>/days/<day>/exercises/<exercise>/sets/",
        "detail": "<set>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {"sets": "<String>", "reps": "<String>", "weight": "<String>"},
            "patch": {"sets": "<String>", "reps": "<String>", "weight": "<String>"},
        },
        "params": None,
    },
    "program": {
        "url": "/user/programs/",
        "detail": "<program>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {"name": "<String>", "startdate": "<date>", "duration": "<Number>"},
            "patch": {
                "name": "<String>",
                "startdate": "<date>",
                "duration": "<Number>",
            },
        },
        "params": None,
    },
    "week": {
        "url": "/user/programs/<program>/weeks/",
        "detail": "<week>/",
        "methods": ["get", "patch"],
        "body": {"post": None, "patch": None},
        "params": None,
    },
    "prg_exercise": {
        "url": "/user/programs/<program>/weeks/<week>/exercises/",
        "detail": "<exercise>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {"name": "<String>", "order": "<String>"},
            "patch": {"name": "<String>"},
        },
        "params": None,
    },
    "prg_secondary": {
        "url": "/user/programs/<program>/weeks/<week>/exercises/<exercise>/secondary/",
        "detail": "add/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "body": {
                "post": {"name": "<String>"},
                "patch": {"name": "<String>"},
            },
        },
        "params": None,
    },
    "prg_set": {
        "url": "/user/programs/<int:order>/weeks/<int:week>/exercises/<int:order>/sets/",
        "detail": "<set>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {"sets": "<String>", "reps": "<String>", "percent": "<Number>"},
            "patch": {"sets": "<String>", "reps": "<String>", "percent": "<Number>"},
        },
        "params": None,
    },
    "library": {
        "url": "/user/library/",
        "detail": "<id>/",
        "methods": ["get", "post", "patch", "delete"],
        "body": {
            "post": {
                "name": "<String>",
                "bodypart": _BODYPART_CHOICES,
                "equipment:": _EQUIPMENT_CHOICES,
                "max": "<Number>",
            },
            "patch": {
                "name": "<String>",
                "bodypart": _BODYPART_CHOICES,
                "equipment:": _EQUIPMENT_CHOICES,
                "max": "<Number>",
                "enabled": "<Boolean>",
            },
        },
        "params": {
            "custom": "<Boolean>",
            "bodypart": _BODYPART_CHOICES,
            "equipment:": _EQUIPMENT_CHOICES,
        },
    },
}

BASIC_ROUTES = {
    "register": {
        "url": "register/",
        "detail": None,
    },
    "login": {
        "url": "login/",
        "detail": None,
    },
    "logout": {
        "url": "logout/",
        "detail": None,
    },
    "refresh": {
        "url": "refresh/",
        "detail": None,
    },
    "delete": {
        "url": "delete/",
        "detail": None,
    },
    "content": {
        "url": "/user/",
        "detail": None,
    },
    "profile": {
        "url": "user/profile/",
        "detail": None,
    },
    "workout": {
        "url": "/user/workouts/",
        "detail": "<wkt_order>/",
    },
    "day": {
        "url": "/user/workouts/<wkt_order>/days/",
        "detail": "<day>/",
    },
    "program": {
        "url": "/user/programs/",
        "detail": "<program>/",
    },
    "week": {
        "url": "/user/programs/<program>/weeks/",
        "detail": "<week>/",
    },
    "wkt_exercise": {
        "url": "/user/workouts/<wkt_order>/days/<day>/exercises/",
        "detail": "<exercise>/",
    },
    "wkt_secondary": {
        "url": "/user/workouts/<wkt_order>/days/<day>/exercises/<exercise>/secondary/",
        "detail": "add/",
    },
    "wkt_set": {
        "url": "/user/workouts/<wkt_order>/days/<day>/exercises/<exercise>/sets/",
        "detail": "<set>/",
    },
    "prg_exercise": {
        "url": "/user/programs/<program>/weeks/<week>/exercises/",
        "detail": "<exercise>/",
    },
    "prg_secondary": {
        "url": "/user/programs/<program>/weeks/<week>/exercises/<exercise>/secondary/",
        "detail": "add/",
    },
    "prg_set": {
        "url": "/user/programs/<int:order>/weeks/<int:week>/exercises/<int:order>/sets/",
        "detail": "<set>/",
    },
    "library": {
        "url": "/user/library/",
        "detail": "<pk>/",
        "params": {
            "custom": "<Boolean>",
            "bodypart": _BODYPART_CHOICES,
            "equipment:": _EQUIPMENT_CHOICES,
        },
    },
    # ---
    "screens": {
        "main": "/user/workouts/active/",
        "workouts": "/user/workouts/",
        "programs": "/user/programs/",
        "settings": "/user/profile/",
    },
}
