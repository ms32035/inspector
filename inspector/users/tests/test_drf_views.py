import pytest

from inspector.users.api.views import UserViewSet
from inspector.users.models import User


class TestUserViewSet:
    @pytest.mark.django_db
    def test_get_queryset(self, user: User, api_rf):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    @pytest.mark.django_db
    def test_me(self, user: User, api_rf):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
