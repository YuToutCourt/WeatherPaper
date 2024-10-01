import os
import subprocess
import tempfile
from threading import Thread

from icecream import ic
from utils.notification_player import play_notification 

def create_playlist_name(current_season, current_weather, time_of_day) -> str:
    """
    Create a playlist name based on the current season, weather, and time of the day
    current_season : str
    current_weather : str
    time_of_day : str
    
    return: playlist_name : str
    """
    return f"{current_season}-{current_weather.replace(' ', '')}-{time_of_day}".lower()

def as_playlist(WALLPAPER_EXE_PATH, playlist_name, n=0):
    """
    Check if the user have the playlist, by setting the wallpaper and checking if the wallpaper has changed.
    If not changed, play a notification to the user.
    playlist_name : str
    n : int
    """
    current_wallpaper = get_wallpaper(WALLPAPER_EXE_PATH)
    set_wallpaper(WALLPAPER_EXE_PATH, playlist_name)
    new_wallpaper = get_wallpaper(WALLPAPER_EXE_PATH)
    ic(current_wallpaper, new_wallpaper, n)
    if current_wallpaper == new_wallpaper and n == 3:
        thread_notif = Thread(target=play_notification, args=(playlist_name,))
        thread_notif.start()
    elif current_wallpaper != new_wallpaper:
        return
    else:
        n += 1
        as_playlist(WALLPAPER_EXE_PATH, playlist_name, n)


def get_wallpaper(WALLPAPER_EXE_PATH):
    """
    Get the current wallpaper using a temporary file to store the output.
    WALLPAPER_EXE_PATH : str

    return: output : str
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_path = tmp_file.name
    try:
        c = f'{WALLPAPER_EXE_PATH} -control getWallpaper > {tmp_path} 2>&1'
        subprocess.run(c, shell=True)
        with open(tmp_path, "r") as file:
            output = file.read()
    finally:
        os.remove(tmp_path)
    return output

def set_wallpaper(WALLPAPER_EXE_PATH, playlist_name):
    """
    Set the wallpaper based on the playlist name
    WALLPAPER_EXE_PATH : str
    playlist_name : str
    """
    command = f'{WALLPAPER_EXE_PATH} -control openPlaylist -playlist {playlist_name}'
    ic(command)
    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True)
        ic(result.stdout)
    except Exception as e:
        ic(e, playlist_name)