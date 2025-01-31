from django.urls import path
from .views import NextSevenDayForecastView, CompareTravelWeatherView

urlpatterns = [
    path(
        "next_seven_day_forecast/",
        NextSevenDayForecastView.as_view(),
        name="next_seven_day_forecast",
    ),
    path(
        "compare_travel_locations_forecast/",
        CompareTravelWeatherView.as_view(),
        name="compare_travel_locations_forecast",
    ),
]
