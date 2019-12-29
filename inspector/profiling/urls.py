from django.urls import path

from . import views

urlpatterns = (
    # urls TableProfile
    path(
        "profile/<int:pk>/",
        views.TableProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path("profile/", views.TableProfileListView.as_view(), name="profile_list"),
    path("table/<int:pk>/", views.TableProfileCreateView.as_view(), name="table_run"),
)
