from random import shuffle

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .constants import CHECK_TYPES, RELATIONS
from .models import Datacheck, CheckRun
from ..base.tests import TestUser
from ..systems.tests import create_system, create_environment

RANDOMS = list(range(10000))
shuffle(RANDOMS)


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    user_no = RANDOMS.pop()
    defaults["username"] = "user-{}".format(user_no)
    defaults["email"] = "user-{}@tempurl.com".format(user_no)
    defaults.update(**kwargs)
    User = get_user_model()
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


def create_datacheck(**kwargs):
    defaults = {}
    defaults["code"] = "datacheck-{}".format(RANDOMS.pop())
    defaults["description"] = "description"
    defaults["weight"] = 1
    defaults["left_type"] = CHECK_TYPES.SQL_QUERY
    defaults["left_logic"] = "left_logic"
    defaults["relation"] = RELATIONS.eq
    defaults["right_type"] = CHECK_TYPES.SQL_QUERY
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


def create_checkrun(**kwargs):
    defaults = {}
    defaults["status"] = "status"
    defaults["result"] = "result"
    defaults["left_value"] = "left_value"
    defaults["right_value"] = "right_value"
    defaults["warning_value"] = "warning_value"
    defaults["error_message"] = "error_message"
    defaults.update(**kwargs)
    if "datacheck" not in defaults:
        defaults["datacheck"] = create_datacheck()
    if "environment" not in defaults:
        defaults["environment"] = create_environment()
    if "user" not in defaults:
        defaults["user"] = create_django_contrib_auth_models_user()
    return CheckRun.objects.create(**defaults)


class DatacheckViewTest(TestCase):
    """
    Tests for Datacheck
    """

    def setUp(self):
        self.client = Client()
        self.test_user = TestUser()
        self.client.login(username="test", password="test")

    def tearDown(self):
        self.test_user.delete()

    def test_list_datacheck(self):
        self.test_user.add_permission(Datacheck, "view_datacheck")
        url = reverse("checks:datacheck_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_datacheck(self):
        self.test_user.add_permission(Datacheck, "add_datacheck")
        url = reverse("checks:datacheck_create")
        data = {
            "code": "code",
            "description": "description",
            "weight": 1,
            "left_type": CHECK_TYPES.SQL_QUERY,
            "left_logic": "left_logic",
            "relation": RELATIONS.eq,
            "right_logic": "right_logic",
            "supports_warning": False,
            "warning_relation": "",
            "warning_type": "",
            "warning_logic": "",
            "left_system": create_system().pk,
            "right_system": create_system().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_detail_datacheck(self):
        self.test_user.add_permission(Datacheck, "view_datacheck")
        datacheck = create_datacheck()
        url = reverse("checks:datacheck_detail", args=[datacheck.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_datacheck(self):
        self.test_user.add_permission(Datacheck, "change_datacheck")
        datacheck = create_datacheck()
        data = {
            "code": "code",
            "description": "description",
            "weight": 1,
            "left_type": "left_type",
            "left_logic": "left_logic",
            "relation": RELATIONS.eq,
            "right_logic": "right_logic",
            "supports_warning": False,
            "warning_relation": "",
            "warning_type": "",
            "warning_logic": "",
            "left_system": create_system().pk,
            "right_system": create_system().pk,
        }
        url = reverse("checks:datacheck_update", args=[datacheck.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class CheckRunViewTest(TestCase):
    """
    Tests for CheckRun
    """

    def setUp(self):
        self.client = Client()
        self.test_user = TestUser()
        self.client.login(username="test", password="test")

    def tearDown(self):
        self.test_user.delete()

    def test_list_checkrun(self):
        self.test_user.add_permission(CheckRun, "view_checkrun")

        url = reverse("checks:checkrun_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_checkrun(self):
        self.test_user.add_permission(CheckRun, "add_checkrun")
        url = reverse("checks:checkrun_create")
        data = {"environment": create_environment(), "id": create_datacheck().pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_detail_checkrun(self):
        self.test_user.add_permission(CheckRun, "view_checkrun")
        checkrun = create_checkrun()
        url = reverse("checks:checkrun_detail", args=[checkrun.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
