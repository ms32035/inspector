import pytest
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from rest_framework.test import APIClient, APIRequestFactory

from inspector.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def api_rf() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def add_permission():
    def inner(user, model, permission_name):
        content_type = ContentType.objects.get_for_model(model)
        permission = Permission.objects.get(content_type=content_type, codename=permission_name)
        user.user_permissions.add(permission)
        user.save()
        user.refresh_from_db()

    return inner


class AuthenticatedClient:
    def __init__(self, user, client):
        self.user = user
        self.client = client

    def add_permission(self, model, permission_name):
        content_type = ContentType.objects.get_for_model(model)
        permission = Permission.objects.get(content_type=content_type, codename=permission_name)
        self.user.user_permissions.add(permission)
        self.user.save()
        self.user.refresh_from_db()


@pytest.fixture
def authenticated_client(user) -> AuthenticatedClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return AuthenticatedClient(user=user, client=client)
