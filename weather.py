from coordinates import get_coordinates
from weather_api_service import get_weather
from printer import format_weather
from exceptions import ApiServiceError, CantGetCoordinates


def main():
    try:
        coordinates = get_coordinates()
    except CantGetCoordinates:
        print('Не удалось получить GPS координаты')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(f'Не удалось получить погоду по координатам {coordinates}')
        exit(1)
    print(format_weather(weather))


if __name__ == '__main__':
    main()
    # print(get_coordinates().longitude, get_coordinates().latitude)
    # print(json.loads(urllib.request.urlopen(OPENWEATHER_URL.format(latitude=get_coordinates().latitude, longitude=get_coordinates().longitude)).read()))
    # print(OPENWEATHER_URL.format(latitude=get_coordinates().latitude, longitude=get_coordinates().longitude))
