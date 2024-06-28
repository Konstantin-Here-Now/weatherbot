from dataclasses import dataclass


@dataclass
class WeatherForecast:
    author: str
    min_temp: float
    max_temp: float
    rain_forecast: str
