from api.hourly_weather import HourlyWeather


class WeatherData:
    def __init__(
        self, author: str, temperatures: list[float], rain_mm: list[float]
    ) -> None:
        self.author = author
        self.temperatures = temperatures
        self.rain_mm = rain_mm

    def get_weather(self) -> dict[int, HourlyWeather]:
        return {
            i: HourlyWeather(self.temperatures[i], self.rain_mm[i]) for i in range(24)
        }
