from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.users import SendCodeAPIView, UserViewSet

router_api_v1 = DefaultRouter()

router_api_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path("v1/", include(router_api_v1.urls)),
    path("v1/activation/", SendCodeAPIView.as_view()),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
