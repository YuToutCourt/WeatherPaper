import subprocess
from icecream import ic

def create_playlist_name(current_season, current_weather, time_of_day) -> str:
    """
    Create a playlist name based on the current season, weather, and time of the day
    current_season : str
    current_weather : str
    time_of_day : str
    
    return: playlist_name : str
    """
    return f"{current_season}-{current_weather.replace(' ', '')}-{time_of_day}".lower()

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
    