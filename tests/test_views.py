import pytest
from django.urls import reverse
from rest_framework import status
from api.models import DistrictsLocations
from api.views import NextSevenDayForecastView, CompareTravelWeatherView


@pytest.mark.django_db
def test_next_seven_day_forecast_view(request_factory, create_district):
    """
    Test the NextSevenDayForecastView to ensure it returns the coolest 10 districts.
    """
    create_district(
        name="District 1",
        bn_name="ঢাকা",
        lat=23.8103,
        long=90.4125,
        division_id=1,
    )
    create_district(
        name="District 2",
        bn_name="ঢাকা",
        lat=24.8103,
        long=91.4125,
        division_id=2,
    )
    url = reverse("next_seven_day_forecast")
    request = request_factory.get(url)
    view = NextSevenDayForecastView.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) <= 10
    assert isinstance(response.data, list)
    for district in response.data:
        assert "average_temp" in district


@pytest.mark.django_db
def test_compare_travel_weather_view(request_factory, create_district):
    """
    Test the CompareTravelWeatherView to ensure it compares weather data for two locations.
    """
    from_dist = create_district(
        name="From District", bn_name="ঢাকা", lat=23.8103, long=90.4125, division_id=1
    )
    to_dist = create_district(
        name="To District", bn_name="ঢাকা", lat=24.8103, long=91.4125, division_id=2
    )
    url = reverse("compare_travel_locations_forecast")
    request = request_factory.get(
        url,
        {
            "from_loc": "From District",
            "to_loc": "To District",
            "max_temp": 30,
            "date": "2023-10-01",
        },
    )
    assert from_dist.name == "From District"
    assert to_dist.name == "To District"
    view = CompareTravelWeatherView.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    for location in response.data:
        assert "average_temp" in location
        assert "can_visit" in location
        assert "travel_date" in location


@pytest.mark.django_db
def test_compare_travel_weather_view_missing_params(request_factory):
    """
    Test the CompareTravelWeatherView with missing query parameters.
    """
    url = reverse("compare_travel_locations_forecast")
    request = request_factory.get(url)
    view = CompareTravelWeatherView.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "message" in response.data


@pytest.mark.django_db
def test_compare_travel_weather_view_invalid_location(request_factory, create_district):
    """
    Test the CompareTravelWeatherView with invalid location names.
    """
    create_district(
        name="Valid District",
        bn_name="ঢাকা",
        lat=23.8103,
        long=90.4125,
        division_id=1,
    )
    url = reverse("compare_travel_locations_forecast")
    request = request_factory.get(
        url,
        {
            "from_loc": "Invalid District",
            "to_loc": "Another Invalid District",
            "max_temp": 30,
            "date": "2023-10-01",
        },
    )
    view = CompareTravelWeatherView.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "message" in response.data


@pytest.mark.django_db
def test_next_seven_day_forecast_view_no_districts(request_factory):
    """
    Test the NextSevenDayForecastView when no districts are found in the database.
    """
    DistrictsLocations.objects.all().delete()
    url = reverse("next_seven_day_forecast")
    request = request_factory.get(url)
    view = NextSevenDayForecastView.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"message": "No districts found in the database."}
