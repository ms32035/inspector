from random import shuffle

import pytest
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from ..systems.tests import create_environment, create_system
from .models import CheckRun, Datacheck, Environment, Instance, System

RANDOMS = list(range(10000))
shuffle(RANDOMS)

pytestmark = pytest.mark.django_db


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    user_no = RANDOMS.pop()
    defaults["username"] = f"user-{user_no}"
    defaults["email"] = f"user-{user_no}@tempurl.com"
    defaults.update(**kwargs)
    user = get_user_model()
    return user.objects.create(**defaults)


def create_datacheck(**kwargs):
    defaults = {}
    defaults["code"] = f"datacheck-{RANDOMS.pop()}"
    defaults["description"] = "description"
    defaults["weight"] = 1
    defaults["left_type"] = Datacheck.CheckTypes.SQL_QUERY
    defaults["left_logic"] = "left_logic"
    defaults["relation"] = Datacheck.Relations.EQ
    defaults["right_type"] = Datacheck.CheckTypes.SQL_QUERY
    defaults["right_logic"] = "right_logic"
    defaults["supports_warning"] = False
    defaults["warning_relation"] = None
    defaults["warning_type"] = None
    defaults["warning_logic"] = "warning_logic"
    defaults.update(**kwargs)
    if "left_system" not in defaults:
        defaults["left_system"] = create_system()
    if "right_system" not in defaults:
        defaults["right_system"] = create_system()
    return Datacheck.objects.create(**defaults)


def create_checkrun(user, **kwargs):
    datacheck = create_datacheck()
    environment = create_environment()
    instance = Instance.objects.create(system=datacheck.left_system, environment=environment)

    defaults = {}
    defaults["status"] = "status"
    defaults["result"] = "result"
    defaults["left_number_value"] = 1
    defaults["right_number_value"] = 2
    defaults["warning_number_value"] = 3
    defaults["error_message"] = "error_message"
    defaults.update(**kwargs)
    if "datacheck" not in defaults:
        defaults["datacheck"] = create_datacheck()
    if "environment" not in defaults:
        defaults["environment"] = create_environment()
    if "user" not in defaults:
        defaults["user"] = user
    defaults["left_instance"] = instance
    return CheckRun.objects.create(**defaults)


class TestDatacheckView:
    """
    Tests for Datacheck
    """

    def test_list_datacheck(self, authenticated_client):
        authenticated_client.add_permission(Datacheck, "view_datacheck")
        url = reverse("checks:datacheck-list")
        response = authenticated_client.client.get(url)
        assert response.status_code == 200

    def test_create_datacheck(self, authenticated_client):
        authenticated_client.add_permission(System, "add_system")
        authenticated_client.add_permission(Environment, "add_environment")
        authenticated_client.add_permission(Datacheck, "add_datacheck")
        url = reverse("checks:datacheck-list")
        data = {
            "code": "code",
            "description": "description",
            "weight": 1,
            "left_type": Datacheck.CheckTypes.SQL_QUERY,
            "left_logic": "left_logic",
            "relation": Datacheck.Relations.EQ,
            "tags": ["tag1", "tag2"],
            "right_type": Datacheck.CheckTypes.SQL_QUERY,
            "right_logic": "right_logic",
            "supports_warning": False,
            "warning_relation": "",
            "warning_type": "",
            "warning_logic": "",
            "left_system": create_system().pk,
            "right_system": create_system().pk,
        }
        response = authenticated_client.client.post(url, data=data)
        assert response.status_code == 201

    def test_detail_datacheck(self, authenticated_client):
        authenticated_client.add_permission(Datacheck, "view_datacheck")
        datacheck = create_datacheck()
        url = reverse("checks:datacheck-detail", args=[datacheck.pk])
        response = authenticated_client.client.get(url)
        assert response.status_code == 200

    def test_update_datacheck(self, authenticated_client):
        authenticated_client.add_permission(Datacheck, "change_datacheck")
        datacheck = create_datacheck()
        data = {
            "code": "code",
            "description": "description",
            "weight": 1,
            "left_type": Datacheck.CheckTypes.SQL_QUERY,
            "left_logic": "left_logic",
            "relation": Datacheck.Relations.EQ,
            "right_logic": "right_logic",
            "supports_warning": False,
            "warning_relation": "",
            "warning_type": "",
            "warning_logic": "",
            "left_system": create_system().pk,
            "right_system": create_system().pk,
        }
        url = reverse("checks:datacheck-detail", args=[datacheck.pk])
        response = authenticated_client.client.patch(url, data)
        assert response.status_code == 200


class TestCheckRunViewTest:
    """
    Tests for CheckRun
    """

    def test_list_checkrun(self, authenticated_client):
        authenticated_client.add_permission(CheckRun, "view_checkrun")

        url = reverse("checks:checkrun-list")
        response = authenticated_client.client.get(url)
        assert response.status_code == 200

    def test_detail_checkrun(self, authenticated_client):
        authenticated_client.add_permission(CheckRun, "view_checkrun")
        checkrun = create_checkrun(authenticated_client.user)
        url = reverse("checks:checkrun-detail", args=[checkrun.pk])
        response = authenticated_client.client.get(url)
        assert response.status_code == 200
