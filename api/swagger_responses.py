# swagger_responses.py
from drf_yasg import openapi

# Swagger documentation for NextSevenDayForecastView
next_seven_day_forecast_docs = {
    "operation_description": """
    Fetch the next 7-day weather forecast for districts and return the coolest 10 districts based on average temperature.
    This endpoint retrieves weather data from the Open-Meteo API and processes it to determine the average temperature for each district.
    """,
    "responses": {
        200: openapi.Response(
            description="Successfully retrieved the coolest 10 districts",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Unique ID of the district",
                        ),
                        "division_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="ID of the division the district belongs to",
                        ),
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Name of the district in English",
                        ),
                        "bn_name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Name of the district in Bengali",
                        ),
                        "lat": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Latitude of the district",
                        ),
                        "long": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Longitude of the district",
                        ),
                        "average_temp": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Average temperature for the district",
                        ),
                    },
                ),
            ),
        ),
        404: openapi.Response(
            description="No districts found in the database.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message indicating no districts were found",
                    ),
                },
            ),
        ),
        500: openapi.Response(
            description="Failed to fetch weather data from the API",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message indicating API failure",
                    ),
                },
            ),
        ),
    },
}

# Swagger documentation for CompareTravelWeatherView
compare_travel_weather_docs = {
    "operation_description": """
    Fetch weather forecasts for specific locations and check if the temperature is within the limit.
    This endpoint compares the weather conditions for two locations (from_loc and to_loc) on a specific date and checks if the temperature is below the specified maximum limit.
    """,
    "manual_parameters": [
        openapi.Parameter(
            name="from_loc",
            in_=openapi.IN_QUERY,
            description="Name of the starting location",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            name="to_loc",
            in_=openapi.IN_QUERY,
            description="Name of the destination location",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            name="max_temp",
            in_=openapi.IN_QUERY,
            description="Maximum allowed temperature (in Celsius)",
            type=openapi.TYPE_NUMBER,
            required=True,
        ),
        openapi.Parameter(
            name="date",
            in_=openapi.IN_QUERY,
            description="Travel date in YYYY-MM-DD format",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    "responses": {
        200: openapi.Response(
            description="Successfully retrieved weather data for the locations",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Unique ID of the location",
                        ),
                        "division_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="ID of the division the location belongs to",
                        ),
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Name of the location in English",
                        ),
                        "bn_name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Name of the location in Bengali",
                        ),
                        "lat": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Latitude of the location",
                        ),
                        "long": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Longitude of the location",
                        ),
                        "average_temp": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Average temperature for the location",
                        ),
                        "can_visit": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="Whether the location can be visited based on the temperature limit",
                        ),
                        "travel_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Travel date in YYYY-MM-DD format",
                        ),
                    },
                ),
            ),
        ),
        400: openapi.Response(
            description="Missing required query parameters",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message indicating missing parameters",
                    ),
                },
            ),
        ),
        404: openapi.Response(
            description="Location not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message indicating the location was not found",
                    ),
                },
            ),
        ),
        500: openapi.Response(
            description="Failed to fetch or process weather data",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message indicating API failure",
                    ),
                },
            ),
        ),
    },
}
