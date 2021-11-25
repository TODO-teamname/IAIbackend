from django.urls import include, path
from rest_framework_nested import routers

from .views import OrganizationViewSet, MembersViewSet

router = routers.SimpleRouter()
router.register(r'organizations', OrganizationViewSet)

members_router = routers.NestedSimpleRouter(router, r'organizations', lookup='organization')
members_router.register(r'members', MembersViewSet, basename='organization-members')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(members_router.urls)),
]
