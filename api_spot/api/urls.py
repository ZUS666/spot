from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    AddSpotsAPIView, EquipmentViewSet, EventViewSet, FavoriteViewSet,
    LocationMapListAPIView, LocationShortListAPIView, LocationViewSet,
    OrderGetViewSet, OrderViewSet, PayView, PlanPhotoAPIView, QuestionViewSet,
    ReviewCreateViewSet, ReviewGetViewSet, RuleViewSet, SpotViewSet,
    SubscireAPIView, UserViewSet,
)


app_name = 'api'

router_api_v1 = DefaultRouter()

router_api_v1.register(r'users', UserViewSet, basename='users')

router_api_v1.register(
    r'locations/(?P<location_id>\d+)/spots/(?P<spot_id>\d+)'
    r'/order/(?P<order_id>\d+)/reviews',
    ReviewCreateViewSet,
    basename='review'
)
router_api_v1.register(
    r'locations/(?P<location_id>\d+)/reviews',
    ReviewGetViewSet,
    basename='get_reviews'
)

router_api_v1.register(
    r'locations/(?P<location_id>\d+)/equipments',
    EquipmentViewSet,
    basename='get_equipments'
)
router_api_v1.register(
    r'locations/(?P<location_id>\d+)/spots/(?P<spot_id>\d+)/order',
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
    basename='locations'
)
router_api_v1.register(
    r'locations/(?P<location_id>\d+)/spots',
    SpotViewSet,
    basename='spots'
)
router_api_v1.register(
    r'events',
    EventViewSet,
    basename='events',
)
router_api_v1.register(
    r'questions',
    QuestionViewSet,
    basename='questions',
)
router_api_v1.register(
    r'rules',
    RuleViewSet,
    basename='rules'
)

view_url = [
    re_path(
        r'locations/(?P<location_id>\d+)/spots/(?P<spot_id>\d+)'
        r'/order/(?P<order_id>\d+)/pay/',
        PayView.as_view(), name='pay'
    ),
    path('short_locations/', LocationShortListAPIView.as_view()),
    path('map_locations/', LocationMapListAPIView.as_view()),
    path('subscribe', SubscireAPIView.as_view(
        {'post': 'post', 'delete': 'delete'}
    )),
    re_path(
        r'locations/(?P<location_id>\d+)/plan_photo/',
        PlanPhotoAPIView.as_view()
    ),
    re_path(
        r'locations/(?P<location_id>\d+)/favorite/',
        FavoriteViewSet.as_view(
            {'post': 'create', 'delete': 'delete'})),
    re_path(
        r'locations/(?P<location_id>\d+)/add_spots/',
        AddSpotsAPIView.as_view()),
]

urlpatterns = [
    path('v1/', include(view_url)),
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
