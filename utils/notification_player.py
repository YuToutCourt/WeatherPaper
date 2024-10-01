import ctypes

def play_notification(playlist_name: str):
    """
    Play a notification sound when the playlist is not found
    playlist_name : str
    """

    ctypes.windll.user32.MessageBoxW(0, f"You have no playlist named {playlist_name}", '[WeatherPaper] Playlist not found', 0x40 | 0x0)
