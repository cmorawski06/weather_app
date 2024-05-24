import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from weather_api.models import UserPreferences, Location
from django.views.decorators.http import require_POST
import requests
import os

# Create your views here.

def login_view(request):
    notNavbar = True
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Przekierowanie użytkownika na stronę po zalogowaniu
            return redirect('home')
        else:
            # Obsługa błędnego logowania
            return render(request, 'auth/login.html', {'error_message': 'Nieprawidłowy login lub hasło.'})
    else:
        return render(request, 'auth/login.html', {'navbar': notNavbar})
    
def register_view(request):
    notNavbar = True
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Sprawdź, czy użytkownik o podanej nazwie użytkownika już istnieje
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nazwa użytkownika jest już zajęta.')
            return redirect('register')
        
        # Stwórz nowego użytkownika
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        messages.success(request, 'Konto zostało pomyślnie utworzone. Możesz teraz się zalogować.')
        return redirect('login')
    else:
        return render(request, 'auth/register.html', {'navbar': notNavbar})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    if request.user.is_authenticated:
        user_preferences = UserPreferences.objects.filter(user=request.user).first()
        favorite_locations = user_preferences.preferred_locations.all() if user_preferences else []
    else:
        favorite_locations = []
    return render(request, 'home.html', {'favorite_locations': favorite_locations})

@login_required
def get_weather_api(request, location):

    # Konfiguracja API (zastąp API_KEY swoim kluczem API)
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={location}&appid={api_key}&units=metric&lang=pl"

    try:
        response = requests.get(complete_url)
        response_data = response.json()

        # Sprawdzamy, czy zapytanie do API było udane
        if response.status_code == 200:
            weather_data = {
                'location': location,
                'temperature': response_data['main']['temp'],
                'description': response_data['weather'][0]['description'],
                'humidity': response_data['main']['humidity'],
                'pressure': response_data['main']['pressure']
            }
        else:
            weather_data = {
                'error': 'Nie udało się pobrać danych pogodowych'
            }
    except requests.RequestException:
        weather_data = {
            'error': 'Błąd połączenia z API pogodowym'
        }

    return JsonResponse(weather_data)

@login_required
def favorite_locations_api(request):
    # Pobierz ulubione lokalizacje aktualnie zalogowanego użytkownika
    user_preferences = UserPreferences.objects.get(user=request.user)
    favorite_locations = user_preferences.preferred_locations.all()

    # Utwórz listę ulubionych lokalizacji w formacie JSON
    favorite_locations_data = []
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    for location in favorite_locations:
        try:
            complete_url = f"{base_url}?q={location}&appid={api_key}&units=metric&lang=pl"
            response = requests.get(complete_url)
            response_data = response.json()
            # Sprawdzamy, czy zapytanie do API było udane
            if response.status_code == 200:
                location_data = {
                    'name': location.name,
                    'temperature': response_data['main']['temp'],
                    'description': response_data['weather'][0]['description'],
                    'humidity': response_data['main']['humidity'],
                    'pressure': response_data['main']['pressure']
                }
            else:
                location_data = {
                    'location': location.name,
                    'error': 'Nie udało się pobrać danych pogodowych'
                }
            favorite_locations_data.append(location_data)
        except requests.RequestException:
            location_data = {
                'location': location.name,
                'error': 'Błąd połączenia z API pogodowym'
            }
            favorite_locations_data.append(location_data)

    # Zwróć listę ulubionych lokalizacji jako odpowiedź JSON
    return JsonResponse({'favorite_locations': favorite_locations_data})

@login_required
def compare_weather_view(request):
    if request.method == 'POST':
        # Pobierz dane z żądania POST
        location1_temperature = request.POST.get('location1_temperature')
        location2_temperature = request.POST.get('location2_temperature')
        # Tutaj możesz przeprowadzić porównanie danych pogodowych
        # i wykonać odpowiednie operacje na nich
        
        # Na razie po prostu zwróć dane do szablonu
        return render(request, 'compare_weather.html', {'location1_temperature': location1_temperature, 'location2_temperature': location2_temperature})
    return render(request, 'compare_weather.html')

@login_required
def check_weather_view(request):
    return render(request, 'check_weather.html', {'OPENWEATHERMAP_API_KEY': os.getenv('OPENWEATHERMAP_API_KEY')})

def empty_view(request):
    return redirect('home')

@login_required
def my_locations_view(request):
    locations = Location.objects.all()
    user_locations = UserPreferences.objects.get(user=request.user).preferred_locations
    user_location_ids = user_locations.values_list('id', flat=True)
    locations = locations.exclude(id__in=user_location_ids)
    return render(request, 'my_locations.html', {'user_locations': user_locations if user_locations.exists() else None, 'locations': locations})

@login_required
@require_POST
def delete_location_api(request):
    # Pobierz indeks lokalizacji do usunięcia z ciała zapytania POST
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    index = json_data['index']

    try:
        # Usuń lokalizację o podanym indeksie dla zalogowanego użytkownika
        user_locations = UserPreferences.objects.get(user=request.user).preferred_locations
        location_to_remove = user_locations.all()[index]
        user_locations.remove(location_to_remove)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
@require_POST
def add_location_api(request):
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    location_id = json_data['location_id']

    try:
        user_locations = UserPreferences.objects.get(user=request.user).preferred_locations
        location_to_add = Location.objects.get(id=location_id)
        user_locations.add(location_to_add)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)