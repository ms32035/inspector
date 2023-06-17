from dj_rest_auth.views import LogoutView
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from .views import GoogleConnect, RegisterUserView, UserProfileView, UserViewSet

router = routers.DefaultRouter()
user = router.register(r"user", UserViewSet)

app_name = "users"
urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("user/me/", UserProfileView.as_view(), name="user-me"),
    path("connect/google/", GoogleConnect.as_view(), name="google_connect"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
]
