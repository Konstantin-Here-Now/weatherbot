from api.open_meteo import get_open_meteo_data
from api.weather_data import WeatherData
from api.weather_forecast import WeatherForecast


async def get_forecasts() -> list[WeatherForecast]:
    weather_datas = await get_api_data()
    forecasts: list[WeatherForecast] = []
    for data in weather_datas:
        forecast = await create_forecast(data)
        forecasts.append(forecast)
    return forecasts


async def get_api_data() -> list[WeatherData]:
    open_meteo_data = await get_open_meteo_data()

    return [open_meteo_data]


async def create_forecast(data: WeatherData) -> WeatherForecast:
    minHour = 6
    maxHour = 21
    max_temp, min_temp = -100.0, 100.0
    not_null_rains: dict[int, float] = {}
    for hour, value in data.get_weather().items():
        if hour < minHour or hour > maxHour:
            continue

        if value.temperature > max_temp:
            max_temp = value.temperature
        if value.temperature < min_temp:
            min_temp = value.temperature

        if value.rain_mm > 0:
            not_null_rains[hour] = value.rain_mm

    rain_forecast = make_rain_forecast(not_null_rains)

    return WeatherForecast(data.author, min_temp, max_temp, rain_forecast)


def make_rain_forecast(rains: dict[int, float]) -> str:
    return "Дождя не будет" if len(rains) == 0 else "Будет дождь"
