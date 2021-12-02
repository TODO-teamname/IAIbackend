from django.urls import include, path
from rest_framework_nested import routers

from .views import OrganizationMoocletViewSet
from organizations.urls import organizations_router

organizations_router.register(r'mooclets', OrganizationMoocletViewSet, basename='mooclets')

urlpatterns = [
        path(r'', include(organizations_router.urls))
]
