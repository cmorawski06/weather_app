from django.db import models

# Create your models here.

from django.db import models

class Location(models.Model):
    """
    Model Location przechowuje informacje o lokalizacji, dla której będą pobierane dane pogodowe.
    
    Atrybuty:
        name (str): Nazwa lokalizacji.
        latitude (Decimal): Szerokość geograficzna lokalizacji.
        longitude (Decimal): Długość geograficzna lokalizacji.
    """
    name = models.CharField(max_length=100)  # Nazwa lokalizacji
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Szerokość geograficzna
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Długość geograficzna

    def __str__(self):
        return self.name

    
class WeatherData(models.Model):
    """
    Model WeatherData przechowuje dane pogodowe dla określonej lokalizacji i daty.
    
    Atrybuty:
        location (Location): Lokalizacja, dla której pobrano dane.
        date (DateField): Data prognozy.
        temperature (float): Temperatura w danej lokalizacji i dniu.
        humidity (float): Wilgotność w danej lokalizacji i dniu.
        wind_speed (float): Prędkość wiatru w danej lokalizacji i dniu.
        description (str): Krótki opis warunków pogodowych.
    """
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Lokalizacja
    date = models.DateField()  # Data prognozy
    temperature = models.FloatField()  # Temperatura
    humidity = models.FloatField()  # Wilgotność
    wind_speed = models.FloatField()  # Prędkość wiatru
    description = models.CharField(max_length=255)  # Opis pogody (np. "słonecznie", "deszczowo")

    class Meta:
        unique_together = ('location', 'date')  # Unikalność na poziomie lokalizacji i daty

    def __str__(self):
        return f"{self.location} - {self.date}"

from django.contrib.auth.models import User

class UserPreferences(models.Model):
    """
    Model UserPreferences przechowuje preferencje użytkownika, takie jak ulubione lokalizacje.
    
    Atrybuty:
        user (User): Użytkownik, którego dotyczą preferencje.
        preferred_locations (ManyToManyField): Ulubione lokalizacje użytkownika.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Użytkownik
    preferred_locations = models.ManyToManyField(Location, blank=True)  # Ulubione lokalizacje

    def __str__(self):
        return f"{self.user.username} Preferences"

class WeatherAlert(models.Model):
    """
    Model WeatherAlert przechowuje informacje o alertach pogodowych dla określonych lokalizacji.
    
    Atrybuty:
        location (Location): Lokalizacja, której dotyczy alert.
        alert_type (str): Typ alertu (np. "Burza", "Ulewa").
        description (str): Opis alertu.
        start_time (DateTimeField): Czas rozpoczęcia alertu.
        end_time (DateTimeField): Czas zakończenia alertu.
    """
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Lokalizacja
    alert_type = models.CharField(max_length=50)  # Typ alertu (np. "Burza", "Ulewa")
    description = models.TextField()  # Opis alertu
    start_time = models.DateTimeField()  # Czas rozpoczęcia alertu
    end_time = models.DateTimeField()  # Czas zakończenia alertu

    def __str__(self):
        return f"{self.alert_type} for {self.location}"

class ForecastSource(models.Model):
    """
    Model ForecastSource przechowuje informacje o różnych źródłach danych pogodowych.
    
    Atrybuty:
        name (str): Nazwa źródła.
        base_url (URLField): URL bazowy API źródła.
        api_key (str): Klucz API do autoryzacji (opcjonalnie).
    """
    name = models.CharField(max_length=100)  # Nazwa źródła
    base_url = models.URLField()  # URL bazowy API źródła
    api_key = models.CharField(max_length=255, blank=True)  # Klucz API (opcjonalnie)

    def __str__(self):
        return self.name