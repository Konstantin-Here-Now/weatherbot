from attr import dataclass


@dataclass
class HourlyWeather:
    temperature: float
    rain_mm: float
