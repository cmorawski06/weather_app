from django.contrib import admin
from .models import Location, WeatherData, UserPreferences, WeatherAlert, ForecastSource

# Register your models here.

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('location', 'date', 'temperature', 'humidity', 'wind_speed', 'description')
    list_filter = ('location', 'date')
    search_fields = ('location__name', 'description')

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('location', 'alert_type', 'start_time', 'end_time')
    list_filter = ('alert_type', 'location')
    search_fields = ('location__name', 'alert_type')

@admin.register(ForecastSource)
class ForecastSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')
    search_fields = ('name',)