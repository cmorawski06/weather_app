"""
URL configuration for weather_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from weather_api import views

urlpatterns = [
    path('', views.empty_view),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),  # Widok logowania
    path('logout/', views.logout_view, name='logout'),  # Widok wylogowania
    path('register/', views.register_view, name='register'),  # Widok rejestracji
    path('home/', views.home_view, name='home'),
    path('api/favorite_locations/', views.favorite_locations_api, name='favorite_locations_api'),
    path('api/weather/<str:location>', views.get_weather_api, name='get_weather_api'),
    path('compare-weather/', views.compare_weather_view, name='compare_weather'),
    path('check-weather/', views.check_weather_view, name='check_weather'),
    path('my-locations/', views.my_locations_view, name='my_locations'),
    path('api/delete-location/', views.delete_location_api, name='delete_location_api'),
    path('api/add-location/', views.add_location_api, name='add_location_api')
]
