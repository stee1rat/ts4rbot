# -*- coding: utf-8 -*-

import datetime

import random
import re
import requests

import settings

from constants import who, who_quotes, weather_icons
from geopy.geocoders import Nominatim
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telegram import ParseMode
from pprint import pprint

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

OWM_KEY = settings.OWM_KEY

owm = OWM(OWM_KEY)
config_dict = get_default_config()
config_dict['language'] = 'ru'
config_dict['units'] = "celsius"


def info(update, context):
    save_username(update, context)
    answer = f"Вероятность составляет: {random.randrange(100)}%"
    update.message.reply_text(answer)


def save_username(update, context):
    if 'users' not in context.chat_data:
        context.chat_data['users'] = {}
    if update.message.from_user.username not in context.chat_data['users']:
        context.chat_data['users'][update.message.from_user.username] = ''


def weather(update, context):
    city = re.sub('Царь.*погода', '', update.message.text, flags=re.I)
    city = city.strip().lower()

    geolocator = Nominatim(user_agent="ts4rbot")
    address = geolocator.geocode(city)
    lat = address.latitude
    lon = address.longitude

    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat, lon).weather
    weather = observation.temperature('celsius')

    answer = '`'
    answer += city.capitalize()
    answer += "\n"
    answer += f"{weather_icons[observation.weather_icon_name]} "

    answer += f"{round(weather['temp'])}°C\n"
    answer += f"{observation.detailed_status}\n".capitalize()
    answer += f"\nОщущается как {round(weather['feels_like'])}°C\n"
    sunrise = datetime.datetime.fromtimestamp(observation.sunrise_time())
    answer += f"Восход в {sunrise.strftime('%H:%M')}\n"
    sunset = datetime.datetime.fromtimestamp(observation.sunset_time())
    answer += f"Закат в {sunset.strftime('%H:%M')}"
    answer += "\n"

    weather_url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OWM_KEY,
        "units": "metric",
        "lang": "ru",
        "exclude": "minutely,hourly"
    }

    result = requests.get(weather_url, params=params)
    weather = result.json()

    for day in weather['daily']:
        d = datetime.datetime.fromtimestamp(day['dt'])
        answer += '\n'
        answer += d.strftime('%a, %b %d') + ' '
        answer += weather_icons[day['weather'][0]['icon']] + ' '
        answer += str(round(day['temp']['day'])) + "°C"

    answer += '`'
    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN
    )


def whoami(update, context):
    save_username(update, context)

    extension = random.choice(who[2]) if random.randrange(3) == 2 else ''

    name = extension['0'] + ' ' if '0' in extension else ''
    name += random.choice(who[0]) + ' ' + random.choice(who[1])
    name += ' ' + extension['1'] if '1' in extension else ''

    context.chat_data['users'][update.message.from_user.username] = name
    answer = f"@{update.message.from_user.username}, вы — {name}"
    update.message.reply_text(answer, quote=False)


def whois(update, context):
    save_username(update, context)
    who = re.sub('Царь.*кто', '', update.message.text, flags=re.I)
    who = who.replace('?', '').strip().lower()
    who = random.choice(who_quotes) + ' ' + who + ' - @'
    who += random.choice(list(context.chat_data['users'].keys()))
    update.message.reply_text(who.capitalize(), quote=False)


def whostats(update, context):
    save_username(update, context)
    answer = ''
    for user, name in context.chat_data['users'].items():
        if name:
            answer += f"*{user}* - {name}\n"
    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN
    )

