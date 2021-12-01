from django.urls import include, path
from rest_framework_nested import routers

from .views import MoocletViewSet

router = routers.DefaultRouter()
router.register(r'organizations', MoocletViewSet)

urlpatterns = [
        path(r'', include(router.urls))
]
