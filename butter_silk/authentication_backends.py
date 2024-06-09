# authentication_backends.py
from django.apps import apps
from django.contrib.auth.backends import BaseBackend

# Get the Staff model
Staff = apps.get_model('staff', 'Staff')

class StaffBackend(BaseBackend):
    def authenticate(self, request, staff_id=None, password=None, **kwargs):
        try:
            staff = Staff.objects.get(staff_id=staff_id)
            if staff.check_password(password):
                return staff
        except Staff.DoesNotExist:
            return None

    def get_user(self, staff_id):
        try:
            return Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return None
