from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, OrderGetViewSet, OrderViewSet,
                    ReviewCreateViewSet, ReviewGetViewSet,
                    LocationViewSet, UserViewSet)


app_name = 'api'

router_api_v1 = DefaultRouter()

router_api_v1.register(r'users', UserViewSet, basename='users')

router_api_v1.register(
    r'orders/(?P<order_id>\d+)/reviews',
    ReviewCreateViewSet,
    basename='review'
)
router_api_v1.register(
    r'spots/(?P<spot_id>\d+)/reviews',
    ReviewGetViewSet,
    basename='get_reviews'
)

router_api_v1.register(
    r'locations/(?P<location_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)
router_api_v1.register(
    r'locations/(?P<location_id>\d+)/order',
    OrderViewSet,
    basename='order'
)
router_api_v1.register(
    'orders',
    OrderGetViewSet,
    basename='get_orders'
)
router_api_v1.register(
    r'locations',
    LocationViewSet,
    basename='favorite'
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
