from random import shuffle

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from .constants import APPLICATIONS
from .models import System, Environment, Instance
from ..base.tests import TestUser

RANDOMS = list(range(10000))
shuffle(RANDOMS)


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_system(**kwargs):
    defaults = {}
    defaults["name"] = "system-{}".format(RANDOMS.pop())
    defaults["application"] = APPLICATIONS.POSTGRES
    defaults.update(**kwargs)
    return System.objects.create(**defaults)


def create_environment(**kwargs):
    defaults = {}
    defaults["name"] = "environment-{}".format(RANDOMS.pop())
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


class SystemViewTest(TestCase):
    """
    Tests for System
    """

    def setUp(self):
        self.client = Client()
        self.test_user = TestUser()
        self.client.login(username="test", password="test")
        self.system = None

    def tearDown(self):
        self.test_user.delete()

    def test_list_system(self):
        self.test_user.add_permission(System, "view_system")
        create_system()
        url = reverse("systems:system_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_system(self):
        self.test_user.add_permission(System, "add_system")
        url = reverse("systems:system_create")
        data = {"name": "name", "application": "application"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_system(self):
        self.test_user.add_permission(System, "change_system")
        system = create_system()
        data = {"name": "name", "application": "application"}
        url = reverse("systems:system_update", args=[system.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class EnvironmentViewTest(TestCase):
    """
    Tests for Environment
    """

    def setUp(self):
        self.client = Client()
        self.test_user = TestUser()
        self.client.login(username="test", password="test")

    def tearDown(self):
        self.test_user.delete()

    def test_list_environment(self):
        self.test_user.add_permission(Environment, "view_environment")
        url = reverse("systems:environment_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_environment(self):
        self.test_user.add_permission(Environment, "add_environment")
        url = reverse("systems:environment_create")
        data = {"name": "environment-{}".format(RANDOMS.pop())}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_update_environment(self):
        self.test_user.add_permission(Environment, "change_environment")
        environment = create_environment()
        data = {"name": "environment-{}".format(RANDOMS.pop())}
        url = reverse("systems:environment_update", args=[environment.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class InstanceViewTest(TestCase):
    """
    Tests for Instance
    """

    def setUp(self):
        self.client = Client()
        self.test_user = TestUser()
        self.client.login(username="test", password="test")

    def tearDown(self):
        self.test_user.delete()

    def test_list_instance(self):
        self.test_user.add_permission(Instance, "view_instance")
        url = reverse("systems:instance_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_instance(self):
        self.test_user.add_permission(Instance, "add_instance")
        url = reverse("systems:instance_create")
        data = {
            "host": "host",
            "port": 1000,
            "db": "database",
            "login": "login",
            "password": "password",
            "system": create_system().pk,
            "environment": create_environment().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_instance(self):
        self.test_user.add_permission(Instance, "view_instance")
        self.system = create_system()
        self.instance = create_instance(system=self.system)
        url = reverse("systems:instance_detail", args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_instance(self):
        self.test_user.add_permission(Instance, "change_instance")
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
        url = reverse("systems:instance_update", args=[instance.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
