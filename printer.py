from datetime import datetime

from weather_api_service import Weather, WeatherType


def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return f'{weather.city}, {weather.weather_type.value}\n' \
           f'Температура: {weather.temperature}°C, ощущается как {weather.temp_feels}°C\n' \
           f'' \
           f'Влажность: {weather.humidity}%\n' \
           f'Ветер: {weather.wind_speed} м/с\n' \
           f'Восход: {weather.sunrise.strftime("%H:%M")}\n' \
           f'Закат: {weather.sunset.strftime("%H:%M")}'


if __name__ == '__main__':
    print(format_weather(Weather(temperature=-8, weather_type=WeatherType.CLOUDS, sunrise=datetime(2023, 2, 6, 7, 25, 27), sunset=datetime(2023, 2, 6, 17, 6, 18), city='Красный Октябрь')
))