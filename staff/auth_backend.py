from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import Staff


class StaffBackend(
    ModelBackend
):  # Inherit from ModelBackend to handle both staff and superuser logins
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if it's a superuser
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        # If not a superuser, check if it's a staff member
        try:
            staff = Staff.objects.get(staff_id=username, phone=password)
            user, created = User.objects.get_or_create(username=staff.staff_id)
            if created:
                user.set_unusable_password()  # Ensure they can't log in with a regular password
                user.save()
            return user
        except Staff.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
