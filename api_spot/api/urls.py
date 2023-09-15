from django.urls import include, path
from rest_framework import routers

from api.views.review import ReviewGetViewSet, ReviewCreateViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'orders/(?P<order_id>\d+)/reviews',
    ReviewCreateViewSet,
    basename='review'
)
router_v1.register(
    r'spots/(?P<spot_id>\d+)/reviews',
    ReviewGetViewSet,
    basename='get_reviews'
)

# router_v1.register(
#     r'locations/(?P<location_id>\d+)/favorite',
#     FavoriteViewSet,
#     basename='favorite'
# )
# router_v1.register(
#     r'/spots/(?P<spot_id>\d+)/order',
#     ReservationViewSet,
#     basename='reservation'
# )

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router_v1.urls)),
]
