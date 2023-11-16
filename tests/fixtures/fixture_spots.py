import datetime
import itertools

import pytest
from model_bakery import baker

from spots.constants import MEETING_ROOM, WORK_SPACE
from spots.models import Location, Spot


@pytest.fixture
def prices():
    return baker.make(
        'spots.Price', price=itertools.cycle((100, 200)), _quantity=2
    )


@pytest.fixture
def location():
    return Location.objects.create(
        name='first_location',
        open_time=datetime.time(6, 0, 0),
        close_time=datetime.time(22, 0, 0),
        street='street1',
        house_number=1,
        metro='metro1',
        city='city1',
        latitude=55.55,
        longitude=54.54,
        days_open='Пн-Пт',
    )


@pytest.fixture
def spots(location, prices):
    equipments = baker.make('spots.Equipment', _quantity=3)
    workspaces = [Spot.objects.create(
        name=f'workspace {i}',
        price_id=prices[0].id,
        location_id=1,
        category=WORK_SPACE,
        description='description workspace {i}',
    ) for i in range(3)]
    meeting_rooms = [Spot.objects.create(
        name=f'meeting room {i}',
        price_id=prices[1].id,
        location_id=1,
        category=MEETING_ROOM,
        description='description meeting room {i}',
    ) for i in range(2)]
    for spot in workspaces:
        spot.equipment.add(equipments[0], equipments[1])
    for spot in meeting_rooms:
        spot.equipment.add(equipments[0], equipments[2])
    return (workspaces, meeting_rooms)
