from django.urls import include, path
from rest_framework_nested import routers

from organizations.views import OrganizationViewSet, MembersViewSet
from organizations.urls import organizations_router


organizations_router.register(r'mooclets', MembersViewSet, basename='mooclets')

urlpatterns = [
    path(r'', include(organizations_router.urls)),
]
