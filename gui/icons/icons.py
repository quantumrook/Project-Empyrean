"""Helper module to standardize access to icon graphics.
"""
from utils.private.private import directory_paths

png_icons = {
    "popout"    : f'{directory_paths["icons"]}\\expand-in-new-window.png',  
    #https://www.flaticon.com/free-icons/pop-out created by Freepik - Flaticon
    #"download"  : f'{directory_paths["icons"]}\\download.png',              
    #https://www.flaticon.com/free-icons/obtain  created by meaicon - Flaticon
    "download"  : f'{directory_paths["icons"]}\\wi-cloud-down.png',
    "splash"    : f'{directory_paths["icons"]}\\quantumrook_2.png'
}

svg_icons = {
    "wi-cloud-down" : f'{directory_paths["icons"]}\\weather-icons-svg\\wi-cloud-down.svg'
}

class ClockKeys():
    """Helper class for mapping dictionary key names to file names
    """
    wi_time_1 = "wi-time-1"
    wi_time_2 = "wi-time-2"
    wi_time_3 = "wi-time-3"
    wi_time_4 = "wi-time-4"
    wi_time_5 = "wi-time-5"
    wi_time_6 = "wi-time-6"
    wi_time_7 = "wi-time-7"
    wi_time_8 = "wi-time-8"
    wi_time_9 = "wi-time-9"
    wi_time_10 = "wi-time-10"
    wi_time_11 = "wi-time-11"
    wi_time_12 = "wi-time-12"

clock_icons = {
    "wi-time-1" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_1}.png',
    "wi-time-2" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_2}.png',
    "wi-time-3" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_3}.png',
    "wi-time-4" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_4}.png',
    "wi-time-5" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_5}.png',
    "wi-time-6" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_6}.png',
    "wi-time-7" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_7}.png',
    "wi-time-8" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_8}.png',
    "wi-time-9" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_9}.png',
    "wi-time-10" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_10}.png',
    "wi-time-11" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_11}.png',
    "wi-time-12" : f'{directory_paths["icons"]}\\clock\\{ClockKeys.wi_time_12}.png'
}

colored_clock_icons = { }

for q in range(0,5):
    for t in range(1,13):
        name = f'wi-time-{t}-g-{q}q'
        colored_clock_icons[name] = f'{directory_paths["icons"]}\\clock\\{name}.png'
