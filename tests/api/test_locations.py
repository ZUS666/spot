import pytest
from rest_framework import status


@pytest.mark.django_db
class TestLocations:
    """
    Тесты эндпоинтов группы locations.
    """
    url_locations = '/api/v1/locations/'
    url_map_locations = '/api/v1/map_locations/'
    url_short_locations = '/api/v1/short_locations/'

    def test_get_locations(self, unauthed_client, location, spots, prices):
        response = unauthed_client.get(self.url_locations)
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        low_price = min(prices, key=lambda i: i.total_price).total_price
        address = (f'г. {location.city}, {location.street}, '
                   f'{location.house_number}')
        expected_data = {
            'name': location.name,
            'open_time': location.open_time.strftime('%H:%M'),
            'close_time': location.close_time.strftime('%H:%M'),
            'metro': location.metro,
            'get_full_address_str': address,
            'days_open': location.days_open,
            'count_workspace': len(spots[0]),
            'count_meeting_room': len(spots[1]),
            'low_price': low_price,
            'coordinates': [location.latitude, location.longitude],
        }
        response_data = response.json()[0]
        for key, value in expected_data.items():
            assert response_data.get(key) == value, (
                f'{key}: {response_data.get(key)} not equal {value}'
            )
