from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class DummyUser:
    EMAIL = "test@test.com"
    PASSWORD = "test"

    def __init__(self):
        self.user = get_user_model().objects.create_user(email=self.EMAIL, password=self.PASSWORD)

    def add_permission(self, model, permission_name):
        content_type = ContentType.objects.get_for_model(model)
        permission = Permission.objects.get(content_type=content_type, codename=permission_name)
        self.user.user_permissions.add(permission)
        self.user.save()
        self.user.refresh_from_db()

    def login(self, client):
        client.login(email=self.EMAIL, password=self.PASSWORD)

    def delete(self):
        self.user.delete()
