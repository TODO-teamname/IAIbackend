from django.conf.urls import include
from django.urls import path
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'mooclet', views.MoocletCreate, 'mooclet')

urlpatterns = [
    # path('api/mooclet/', include(router.urls)),
    path('api/mooclet/django_model', views.MoocletCreate.as_view()),
    path('api/mooclet/', views.process_mooclet),  # params for POST: mooclet_name, policy_id; params for GET: mooclet_id
    path('download/', views.download_data),
]
