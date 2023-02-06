from datetime import datetime
from enum import Enum
from typing import NamedTuple, Literal, TypeAlias
import urllib.request
from urllib.error import URLError
import json
from json.decoder import JSONDecodeError
import ssl

import config
from coordinates import Coordinates
from exceptions import ApiServiceError

Celsius: TypeAlias = int
Percents: TypeAlias = int


class WeatherType(str, Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморось'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    MIST = 'Туман'
    CLOUDS = 'Облачно'


class Weather(NamedTuple):
    temperature: Celsius
    temp_feels: Celsius
    weather_type: WeatherType
    humidity: Percents
    wind_speed: int | float
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        latitude=coordinates.latitude, longitude=coordinates.longitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temp(openweather_dict),
        temp_feels=_parse_temp_feels(openweather_dict),
        humidity=_parse_humidity(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        wind_speed=_parse_wind_speed(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
        city=_parse_city(openweather_dict)
    )


def _parse_temp(openweather_dict: dict) -> Celsius:
    try:
        return round(openweather_dict['main']['temp'])
    except KeyError:
        raise ApiServiceError


def _parse_temp_feels(openweather_dict: dict) -> Celsius:
    try:
        return round(openweather_dict['main']['feels_like'])
    except KeyError:
        raise ApiServiceError


def _parse_humidity(openweather_dict: dict) -> Percents:
    return round(openweather_dict['main']['humidity'])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError

    weather_types = {
        '2': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.MIST,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_wind_speed(openweather_dict: dict) -> float | int:
    return openweather_dict['wind']['speed']


def _parse_sun_time(openweather_dict: dict, time: Literal['sunrise', 'sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict['name']


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=0, longitude=0)))
