import pytest
from django.test import RequestFactory
from api.models import DistrictsLocations


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def create_district():
    def test_create_district(**kwargs):
        return DistrictsLocations.objects.create(**kwargs)

    return test_create_district
