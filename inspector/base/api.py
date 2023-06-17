from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer
from rest_framework.views import exception_handler


class AuthPermission(permissions.BasePermission):
    perms = None

    def has_permission(self, request, view):
        if not request.user or (not request.user.is_authenticated and self.authenticated_users_only):
            return False

        return request.user.has_perms([self.perms])


class PageNumberWithPageSizePagination(PageNumberPagination):
    page_size_query_param = "page_size"


def ra_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            response.data["message"] = str(response.data)
        else:
            response.data = {"message": str(response.data)}

    return response


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class EmptySerializer(Serializer):
    """Hack around Spectacular bug"""
