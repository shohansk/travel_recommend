import pandas as pd
import requests_cache
import openmeteo_requests
from retry_requests import retry
from core.settings import config
from rest_framework import status
from .models import DistrictsLocations
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .swagger_responses import next_seven_day_forecast_docs, compare_travel_weather_docs


class BaseWeatherView(APIView):
    """
    Base class for weather-related views with common functionality.
    """

    @staticmethod
    def setup_openmeteo_client():
        """
        Initializes and returns an Open-Meteo API client with caching and retries.
        """
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        return openmeteo_requests.Client(session=retry_session)

    @staticmethod
    def fetch_weather_data(openmeteo_client, lats, longs, date=None):
        """
        Fetches weather data from the Open-Meteo API for given latitudes, longitudes, and optional date.
        """
        url = config.base.OPEN_METEO_API_URL
        params = {"latitude": lats, "longitude": longs, "hourly": "temperature_2m"}
        if date:
            params["start_date"] = date
            params["end_date"] = date
        return openmeteo_client.weather_api(url, params=params)

    @staticmethod
    def process_weather_response(response):
        """
        Processes the weather API response and calculates the average temperature.
        """
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ),
            "temperature_2m": hourly_temperature_2m,
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        filtered_df = hourly_dataframe[
            hourly_dataframe["date"].dt.time == pd.to_datetime("08:00:00").time()
        ]
        return filtered_df["temperature_2m"].mean()

    @staticmethod
    def search_location(location_name):
        """
        Searches for a location in the database by name.
        """
        try:
            return (
                DistrictsLocations.objects.filter(name__iexact=location_name)
                .values("id", "division_id", "name", "bn_name", "lat", "long")
                .first()
            )
        except Exception as e:
            print(f"Error searching for location: {e}")
            return None


class NextSevenDayForecastView(BaseWeatherView):
    """
    API view to fetch the next 7-day weather forecast for districts.
    """

    @staticmethod
    def fetch_and_serialize_districts():
        """
        Fetches and serializes district data from the database.
        """
        districts = DistrictsLocations.objects.all().values(
            "id", "division_id", "name", "bn_name", "lat", "long"
        )
        if not districts:
            return None
        return list(districts)

    @swagger_auto_schema(**next_seven_day_forecast_docs)
    def get(self, request):
        """
        Handles GET requests to fetch the next 7-day weather forecast for districts.
        Returns the coolest 10 districts based on average temperature.
        """
        # Fetch and serialize district data
        district_data = self.fetch_and_serialize_districts()
        if not district_data:
            return Response(
                {"message": "No districts found in the database."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Extract latitudes and longitudes
        lats = [dis["lat"] for dis in district_data]
        longs = [dis["long"] for dis in district_data]

        # Fetch and process weather data
        try:
            openmeteo = self.setup_openmeteo_client()
            responses = self.fetch_weather_data(openmeteo, lats, longs)
            for index, response in enumerate(responses):
                district_data[index]["average_temp"] = self.process_weather_response(
                    response
                )
        except Exception as e:
            print(f"API request failed: {e}")
            return Response(
                {"message": "Failed to fetch weather data from the API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        sorted_districts = sorted(district_data, key=lambda x: x["average_temp"])[:10]
        return Response(sorted_districts, status=status.HTTP_200_OK)


class CompareTravelWeatherView(BaseWeatherView):
    """
    API view to fetch weather forecasts for specific locations and check if the temperature is within the limit.
    """

    @staticmethod
    def validate_query_params(request):
        """
        Validates the required query parameters.
        """
        from_loc = request.query_params.get("from_loc")
        to_loc = request.query_params.get("to_loc")
        max_temp = request.query_params.get("max_temp")
        date = request.query_params.get("date")
        if not all([from_loc, to_loc, max_temp, date]):
            return Response(
                {
                    "message": "`from_loc`, `to_loc`, `max_temp`, and `date` are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return from_loc, to_loc, max_temp, date

    @staticmethod
    def prepare_location_data(from_loc, to_loc):
        """
        Searches for locations in the database and returns their data.
        """
        from_dist = BaseWeatherView.search_location(from_loc)
        to_dist = BaseWeatherView.search_location(to_loc)
        if not from_dist or not to_dist:
            return Response(
                {"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return from_dist, to_dist

    @staticmethod
    def process_and_sort_locations(responses, from_dist, to_dist, max_temp, date):
        """
        Processes weather data and sorts locations by average temperature.
        """
        locations = [from_dist, to_dist]
        for index, response in enumerate(responses):
            try:
                average_temp = BaseWeatherView.process_weather_response(response)
                locations[index]["average_temp"] = average_temp
                locations[index]["can_visit"] = average_temp <= float(max_temp)
                locations[index]["travel_date"] = date
            except Exception as e:
                print(f"Error processing weather data for location {index}: {e}")
        return sorted(locations, key=lambda x: x["average_temp"])

    @swagger_auto_schema(**compare_travel_weather_docs)
    def get(self, request):
        """
        Handles GET requests to fetch weather forecasts for specific locations.
        """
        validation_result = self.validate_query_params(request)
        if isinstance(validation_result, Response):
            return validation_result
        from_loc, to_loc, max_temp, date = validation_result
        location_result = self.prepare_location_data(from_loc, to_loc)
        if isinstance(location_result, Response):
            return location_result
        from_dist, to_dist = location_result
        try:
            openmeteo = self.setup_openmeteo_client()
            lats = [from_dist["lat"], to_dist["lat"]]
            longs = [from_dist["long"], to_dist["long"]]
            responses = self.fetch_weather_data(openmeteo, lats, longs, date)
            sorted_data = self.process_and_sort_locations(
                responses, from_dist, to_dist, max_temp, date
            )
        except Exception as e:
            print(f"Failed to fetch or process weather data: {e}")
            return Response(
                {"message": "Failed to fetch or process weather data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(sorted_data, status=status.HTTP_200_OK)
