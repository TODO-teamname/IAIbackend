from rest_framework import routers
from django.urls import path, include
from .views import MoocletViewSet

router = routers.DefaultRouter()
router.register(r'mooclet', MoocletViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]

