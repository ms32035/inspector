from django.urls import resolve, reverse


def test_user_me():
    assert reverse("api:user-me") == "/api/v1/user/me/"
    assert resolve("/api/v1/user/me/").view_name == "api:user-me"
