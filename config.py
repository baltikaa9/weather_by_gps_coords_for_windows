import os

from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API = os.getenv('OPENWEATHER_API')
OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?' \
                  'lat={latitude}&lon={longitude}&appid=' + OPENWEATHER_API + '&lang=ru' \
                  '&units=metric'
