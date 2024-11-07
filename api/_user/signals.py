from django.dispatch import Signal

# New user has registered.
user_registered = Signal()

# User activated their account.
user_activated = Signal()

# User has been updated.
user_updated = Signal()
