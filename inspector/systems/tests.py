from random import shuffle

import pytest
from rest_framework.reverse import reverse

from .models import Environment, Instance, System

RANDOMS = list(range(10000))
shuffle(RANDOMS)

pytestmark = pytest.mark.django_db


def create_system(**kwargs):
    defaults = {}
    defaults["name"] = f"system-{RANDOMS.pop()}"
    defaults["application"] = System.Applications.POSTGRES
    defaults.update(**kwargs)
    return System.objects.create(**defaults)


def create_environment(**kwargs):
    defaults = {}
    defaults["name"] = f"environment-{RANDOMS.pop()}"
    defaults.update(**kwargs)
    return Environment.objects.create(**defaults)


def create_instance(**kwargs):
    defaults = {}
    defaults["host"] = "host"
    defaults["port"] = 100
    defaults["db"] = "database"
    defaults["login"] = "login"
    defaults["password"] = "password"
    defaults.update(**kwargs)
    if "system" not in defaults:
        defaults["system"] = create_system()
    if "environment" not in defaults:
        defaults["environment"] = create_environment()
    return Instance.objects.create(**defaults)


class TestSystemView:
    """
    Tests for System
    """

    def test_list_system(self, authenticated_client):
        authenticated_client.add_permission(System, "view_system")
        create_system()
        url = reverse("systems:system-list")
        response = authenticated_client.client.get(url)
        assert response.status_code == 200

    def test_create_system(self, authenticated_client):
        authenticated_client.add_permission(System, "add_system")
        url = reverse("systems:system-list")
        data = {"name": "name", "application": "postgres"}
        response = authenticated_client.client.post(url, data=data)
        assert response.status_code == 201

    def test_update_system(self, authenticated_client):
        authenticated_client.add_permission(System, "change_system")
        system = create_system()
        data = {"name": "new-name", "application": "postgres"}
        url = reverse("systems:system-detail", args=[system.pk])
        response = authenticated_client.client.patch(url, data)
        assert response.status_code == 200


class TestEnvironmentView:
    """
    Tests for Environment
    """

    def test_list_environment(self, authenticated_client):
        authenticated_client.add_permission(Environment, "view_environment")
        url = reverse("systems:environment-list")
        response = authenticated_client.client.get(url)
        assert response.status_code == 200

    def test_create_environment(self, authenticated_client):
        authenticated_client.add_permission(Environment, "add_environment")
        url = reverse("systems:environment-list")
        data = {"name": f"environment-{RANDOMS.pop()}"}
        response = authenticated_client.client.post(url, data=data)
        assert response.status_code == 201

    def test_update_environment(self, authenticated_client):
        authenticated_client.add_permission(Environment, "change_environment")
        environment = create_environment()
        data = {"name": f"environment-{RANDOMS.pop()}"}
        url = reverse("systems:environment-detail", args=[environment.pk])
        response = authenticated_client.client.patch(url, data)
        assert response.status_code == 200


class TestInstanceViewset:
    """
    Tests for Instance
    """

    def test_list_instance(self, authenticated_client):
        authenticated_client.add_permission(Instance, "view_instance")
        url = reverse("systems:instance-list")
        response = authenticated_client.client.get(url)

        assert response.status_code == 200

    def test_create_instance(self, authenticated_client):
        authenticated_client.add_permission(Instance, "add_instance")
        url = reverse("systems:instance-list")
        data = {
            "host": "host",
            "port": 1000,
            "db": "database",
            "login": "login",
            "password": "password",
            "system": create_system().pk,
            "environment": create_environment().pk,
        }
        response = authenticated_client.client.post(url, data=data)

        assert response.status_code == 201

    def test_detail_instance(self, authenticated_client):
        authenticated_client.add_permission(Instance, "view_instance")

        system = create_system()
        instance = create_instance(system=system)
        url = reverse("systems:instance-detail", args=[instance.pk])
        response = authenticated_client.client.get(url)
        assert response.status_code == 200

    def test_update_instance(self, authenticated_client):
        authenticated_client.add_permission(Instance, "change_instance")
        instance = create_instance()
        data = {
            "host": "host",
            "port": 2000,
            "db": "database",
            "login": "login",
            "password": "password",
            "system": create_system().pk,
            "environment": create_environment().pk,
        }
        url = reverse("systems:instance-detail", args=[instance.pk])
        response = authenticated_client.client.patch(url, data)
        assert response.status_code == 200
