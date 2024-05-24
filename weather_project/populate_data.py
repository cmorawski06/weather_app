import os
import django
from datetime import date, datetime
import environ

# Ustawienia Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
django.setup()

from django.contrib.auth.models import User
from weather_api.models import Location, WeatherData, UserPreferences, WeatherAlert, ForecastSource

# Wczytaj zmienne środowiskowe z pliku .env
env = environ.Env()
environ.Env.read_env()

# Ustaw klucze API jako zmienne środowiskowe
OPENWEATHERMAP_API_KEY = env('OPENWEATHERMAP_API_KEY')
WEATHERAPI_KEY = env('WEATHERAPI_KEY')

# Dodawanie lokalizacji
location1 = Location.objects.create(name='Warsaw', latitude=52.2297, longitude=21.0122)
location2 = Location.objects.create(name='Cracow', latitude=50.0647, longitude=19.9450)
location3 = Location.objects.create(name='Gdansk', latitude=54.3520, longitude=18.6466)

# Dodawanie danych pogodowych
WeatherData.objects.create(location=location1, date=date(2024, 5, 20), temperature=22.5, humidity=60.0, wind_speed=5.5, description='Sunny')
WeatherData.objects.create(location=location1, date=date(2024, 5, 21), temperature=18.0, humidity=70.0, wind_speed=3.0, description='Cloudy')
WeatherData.objects.create(location=location2, date=date(2024, 5, 20), temperature=20.0, humidity=65.0, wind_speed=4.0, description='Partly Cloudy')
WeatherData.objects.create(location=location2, date=date(2024, 5, 21), temperature=19.5, humidity=72.0, wind_speed=4.5, description='Rainy')
WeatherData.objects.create(location=location3, date=date(2024, 5, 20), temperature=16.0, humidity=80.0, wind_speed=6.0, description='Windy')
WeatherData.objects.create(location=location3, date=date(2024, 5, 21), temperature=17.0, humidity=75.0, wind_speed=5.0, description='Clear')

# Tworzenie użytkowników i preferencji
user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')

prefs1 = UserPreferences.objects.create(user=user1)
prefs1.preferred_locations.set([location1, location2])

prefs2 = UserPreferences.objects.create(user=user2)
prefs2.preferred_locations.set([location2, location3])

# Dodawanie alertów pogodowych
WeatherAlert.objects.create(location=location1, alert_type='Storm', description='Severe thunderstorm warning', start_time=datetime(2024, 5, 20, 14, 0), end_time=datetime(2024, 5, 20, 18, 0))
WeatherAlert.objects.create(location=location2, alert_type='Flood', description='Flash flood warning in effect', start_time=datetime(2024, 5, 21, 9, 0), end_time=datetime(2024, 5, 21, 15, 0))
WeatherAlert.objects.create(location=location3, alert_type='Heatwave', description='Extreme heat warning', start_time=datetime(2024, 5, 22, 12, 0), end_time=datetime(2024, 5, 22, 20, 0))

# Dodawanie źródeł prognoz
ForecastSource.objects.create(name='OpenWeatherMap', base_url='http://api.openweathermap.org/data/2.5/', api_key=OPENWEATHERMAP_API_KEY)
ForecastSource.objects.create(name='WeatherAPI', base_url='http://api.weatherapi.com/v1/', api_key=WEATHERAPI_KEY)