import requests
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
from icecream import ic

__all__ = ['get_location_by_ip', 'get_current_season', 'get_current_date', 'get_weather_data', 'get_current_weather', 'get_time_of_day']

def get_location_by_ip() -> tuple:
    """
    Get the location of the user by their IP address
    return: latitude, longitude : tuple
    """
    response = requests.get('https://ipinfo.io')
    data = response.json()
    location = data['loc'].split(',') 
    latitude = location[0]
    longitude = location[1]
    return latitude, longitude

def get_current_season()-> str:
    """
    Get the current season based on the month
    return: season : str
    """
    season = ['winter', 'spring', 'summer', 'fall']
    return season[(datetime.now().month -1) // 3]

def get_current_date() -> str:
    """
    Get the current date in the format YYYY-MM-DD
    return: date : str
    """
    return datetime.now().strftime("%Y-%m-%d")

def get_weather_data(latitude, longitude, start_date, end_date, API_KEY_WEATHER, WEATHER_URL) -> dict:
    """
    Get the weather data for the given location and date
    latitude : float
    longitude : float
    start_date : str
    end_date : str
    API_KEY_WEATHER : str
    WEATHER_URL : str

    return: data : dict
    """
    url = f"{WEATHER_URL}{latitude},{longitude}/{start_date}/{end_date}?key={API_KEY_WEATHER}"
    response = requests.get(url)
    data = response.json()
    ic(response.status_code)

    return data

def get_current_weather(data, hour) -> str:
    """
    Get the current weather based on the hour from the weather data
    data : list[tuple], Ex: [('Overcast', '10:00:00'),('Partially cloudy', '11:00:00')]
    hour : str
    
    return: current weather condition : str
    """
    for values in data:
        if values[1] == hour:
            # Sometimes the weather condition has additional information like 'Rain, Overcast' 
            # so we split the string and get the first word
            return values[0].split(',')[0].strip() 
        
def get_sun_info(latitude, longitude) -> dict[str, datetime]:
    """
    Get the sunrise and sunset time for the given location
    latitude : float
    longitude : float

    return: s : dict
    """
    city = LocationInfo(latitude=latitude, longitude=longitude)
    s = sun(city.observer, date=datetime.now())
    return s

def get_time_of_day():
    """
    Get the time of the day based on the current time
    return: time_of_day : str
    """
    latitude, longitude = get_location_by_ip()
    s = get_sun_info(latitude, longitude)

    current_time = datetime.now().time()
    sunrise = s['sunrise'].time()
    sunset = s['sunset'].time()

    if current_time < sunrise:
        return "Night"
    elif sunrise <= current_time < (sunrise.replace(hour=sunrise.hour + 1)):
        return "Sunrise"
    elif current_time < sunset:
        return "Day"
    elif sunset <= current_time < (sunset.replace(hour=sunset.hour + 1)):
        return "Sunset"
    else:
        return "Night"