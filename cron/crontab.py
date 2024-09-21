from datetime import datetime
from icecream import ic

from weather.weather_api import *
from wallpaper.wallpaper import *

def cron(API_KEY_WEATHER, WEATHER_URL, WALLPAPER_EXE_PATH):
    date = get_current_date()
    location = get_location_by_ip()
    current_season = get_current_season()
    weather_data = get_weather_data(location[0], location[1], date, date, API_KEY_WEATHER, WEATHER_URL)
    values = [(h["conditions"], h["datetime"]) for h in weather_data["days"][0]["hours"]]

    hour = datetime.now().strftime("%H:00:00")
    time_of_day = get_time_of_day()
    current_weather = get_current_weather(values, hour)
    playlist_name = create_playlist_name(current_season, current_weather, time_of_day)

    ic(date, location, current_season, values, hour, time_of_day, current_weather, playlist_name)

    set_wallpaper(WALLPAPER_EXE_PATH, playlist_name)