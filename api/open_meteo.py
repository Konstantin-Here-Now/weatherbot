import aiohttp

from api.weather_data import WeatherData


async def get_open_meteo_data() -> WeatherData:
    request_str = "https://api.open-meteo.com/v1/forecast?latitude=55.7522&longitude=37.6156&hourly=temperature_2m,rain&timezone=Europe%2FMoscow&forecast_days=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(request_str) as response:
            body = await response.json()
            temperatures: list[float] = body["hourly"]["temperature_2m"]  # type: ignore
            rain_mm: list[float] = body["hourly"]["rain"]  # type: ignore
            return WeatherData("Open Meteo", temperatures, rain_mm)
