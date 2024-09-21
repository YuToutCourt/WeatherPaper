import os
import time
import threading
from dotenv import load_dotenv
from icecream import ic
from datetime import datetime
import pystray
from pystray import MenuItem as item
from PIL import Image

from cron.crontab import cron
from utils.logger import output_to_file

load_dotenv()

API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")
WEATHER_URL = os.getenv("WEATHER_URL")
WALLPAPER_EXE_PATH = os.getenv("WALLPAPER_EXE_PATH")

RUNNING = True

def on_clicked(icon, item):
    global RUNNING
    if str(item) == "Quit":
        RUNNING = False
        ic(RUNNING)
        icon.stop()

def load_custom_image(image_path):
    image = Image.open(image_path)
    return image


if __name__ == "__main__":
    ic.configureOutput(
        prefix="[WeatherPaper]", includeContext=True, outputFunction=output_to_file
    )

    icon = pystray.Icon("weather_paper", load_custom_image("./image/logo.ico"), "WeatherPaper", menu=pystray.Menu(
    item('Quit', on_clicked)
    ))

    icon_thread = threading.Thread(target=icon.run)
    icon_thread.start()

    while RUNNING:
        cron(API_KEY_WEATHER, WEATHER_URL, WALLPAPER_EXE_PATH)

        time_to_wait = 3600 - int(datetime.now().strftime("%M")) * 60

        while time_to_wait > 0 and RUNNING:
            time.sleep(1)
            time_to_wait -= 1

    icon_thread.join()