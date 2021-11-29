from django.urls import include, path
from rest_framework_nested import routers

from .views import OrganizationViewSet, MembersViewSet

router = routers.DefaultRouter()
router.register(r'organizations', OrganizationViewSet)

organizations_router = routers.NestedSimpleRouter(router, r'organizations', lookup='organization')
organizations_router.register(r'members', MembersViewSet, basename='members')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(organizations_router.urls)),
]
