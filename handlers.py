# -*- 1oding: utf-8 -*-

import locale
import random
import re
import requests
import sqlite3

from bs4 import BeautifulSoup, Tag
from constants import who, who_quotes, weather_codes
from datetime import datetime
from settings import BOT_NAME
from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import remove_job_if_exists, balaboba
from pprint import pprint

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def anecdote(update, context):
    url = "https://shytok.net/webmaster.php"
    result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    s = result.text.split('\n')[4]
    m = re.search('document.write\(\' (.*) \'\);', s)
    answer = str(m.group(1).replace('<br />', '\n').replace("<br>", "\n"))
    context.bot.send_message(update.effective_message.chat_id, text=answer)


def choose(update, context):
    query = re.sub(
        f"{BOT_NAME}.*выбери", "", update.message.text, flags=re.I)
    options = query.split("или")
    answer = f"Я выбираю: {random.choice(options).strip()}"
    update.message.reply_text(answer)


def fact(update, context):
    url = "https://randstuff.ru/fact/"
    result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(result.text, 'html.parser')
    answer = soup.find('div', id="fact").table.tr.td.text
    context.bot.send_message(update.effective_message.chat_id, text=answer)


def film(update, context):
    query = re.sub(
        f"{BOT_NAME}.*фильм", "", update.message.text, flags=re.I)
    answer = balaboba(query, 9)
    update.message.reply_text(answer)


def apod(update, context):
    url = "http://www.astronet.ru/db/apod.html"
    result = requests.get(
        url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)

    soup = BeautifulSoup(result.text, 'html.parser')
    titles = soup.findAll('p', class_="title")
    article = "http://www.astronet.ru" + titles[0].a.get('href')
    result = requests.get(article, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(result.text, 'html.parser')
    content = soup.find('div', id='content')

    explanation = content.find('b', text='Пояснение:')
    if explanation is None:
        explanation = content.find('b', text='Explanation:')
    cur = explanation.next_sibling

    answer = ''
    while cur.name != 'p':
        if isinstance(cur, Tag):
            for f in cur.findAll('font'):
                f.unwrap()
        answer += re.sub('\s+', ' ', str(cur).replace("\n", ""))
        cur = cur.next_sibling

    context.bot.send_photo(
        update.effective_message.chat_id,
        content.findAll('img')[2].get("src"))

    context.bot.send_message(
        update.effective_message.chat_id,
        text=answer,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True)


def info(update, context):
    answer = f"Вероятность составляет: {random.randrange(100)}%"
    update.message.reply_text(answer)


def instruction(update, context):
    query = re.sub(
        f"{BOT_NAME}.*инструкция", "", update.message.text, flags=re.I)
    answer = balaboba(query, 24)
    update.message.reply_text(answer)


def recipe(update, context):
    query = re.sub(
        f"{BOT_NAME}.*рецепт", "", update.message.text, flags=re.I)
    answer = balaboba(query, 25)
    update.message.reply_text(answer)


def stats(update, context):
    if update.message is None:
        return

    username = update.message.from_user.name
    id = update.message.from_user.id

    if 'users' not in context.chat_data:
        context.chat_data['users'] = {}

    if id not in context.chat_data['users']:
        if username.strip('@') not in context.chat_data['users']:
            # keep this block
            context.chat_data['users'][id] = {
                'username': '',
                'messages': 0,
                'words': 0,
            }
            # ^^ keep this block
        else:
            context.chat_data['users'][id] = {
                'username': username,
                'messages': context.chat_data['users'][username.strip('@')]['messages'],
                'words': context.chat_data['users'][username.strip('@')]['words'],
            }

    if username.strip('@') in context.chat_data['users']:
        del context.chat_data['users'][username.strip('@')]

    context.chat_data['users'][id]['username'] = username
    context.chat_data['users'][id]['messages'] += 1
    context.chat_data['users'][id]['words'] += len(update.message.text)

    pprint(context.chat_data)

    # REMOVE THE CODE BELOW
    if 'quiz_stats' in context.chat_data:
        print("MIGRATION")
        if None in context.chat_data['quiz_stats']:
            del context.chat_data['quiz_stats'][None]
        for (user, data) in context.chat_data['users'].items():
            print(user, data['username'].strip('@'))
            if data['username'].strip('@') in context.chat_data['quiz_stats']:
                print("EXISTS")
                data['quiz'] = context.chat_data['quiz_stats'][data['username'].strip('@')]
                del context.chat_data['quiz_stats'][data['username'].strip('@')]
        #del context.chat_data['quiz_stats'] 


def today(update, context):
    day = datetime.now().day
    month = datetime.now().month
    url = "https://api.wikimedia.org/feed/v1/wikipedia/ru/onthisday/all/"
    url += f"{month}/{day}"
    result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    data = result.json()

    answer = ""
    for holiday in data['holidays']:
        answer += holiday['text'] + "\n"

    answer += "\n"
    for selected in data['selected']:
        answer += f"{selected['year']}: "
        answer += f"{selected['text'].capitalize()}\n"

    update.message.reply_text(answer, quote=False)


def top(update, context):
    data = list(context.chat_data['users'].items())
    sorted_data = sorted(data, key=lambda x: x[1]['words'], reverse=True)
    answer = 'Топ (символы / сообщения):\n\n'
    for i, (user, data) in enumerate(sorted_data):
        # leave only data['username']
        if 'username' not in data:
            name = user
        else:
            name = data['username'].strip('@')
        #name = user if 'username' not in data else data['username']
        answer += f"{i+1}) {name}: {data['words']} / {data['messages']}\n"
    update.message.reply_text(answer, quote=False)


def weather(update, context):
    city = re.sub(f"{BOT_NAME}.*погода", "", update.message.text, flags=re.I)
    city = city.strip().lower()

    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1,
        "accept-language": "russian"
    }

    coordinates = requests.get(nominatim_url, params=params).json()[0]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coordinates['lat'],
        "longitude": coordinates['lon'],
        "daily": {
            "temperature_2m_max",
            "temperature_2m_min",
            "weathercode",
            "sunrise",
            "sunset",
            "apparent_temperature_max",
            "apparent_temperature_min"
        },
        "timezone": "auto",
        "timeformat": "unixtime"
    }

    result = requests.get(weather_url, params=params).json()
    daily = result["daily"]

    answer = '`'
    answer += f"{city.capitalize()}\n\n"

    min = daily['temperature_2m_min'][0]
    max = daily['temperature_2m_max'][0]
    feels_min = daily['apparent_temperature_min'][0]
    feels_max = daily['apparent_temperature_max'][0]

    sunrise = datetime.fromtimestamp(daily['sunrise'][0]).strftime('%H:%M')
    sunset = datetime.fromtimestamp(daily['sunset'][0]).strftime('%H:%M')

    answer += f"{'Сейчас: '}{round((min+max)/2)}°C\n"
    answer += f"{'Ощущается: '}{round((feels_min+feels_max)/2)}°C\n"
    answer += f"{'Восход: '}{sunrise}\n"
    answer += f"{'Закат: '}{sunset}\n\n"

    for i, time in enumerate(daily['time']):
        answer += f"{datetime.fromtimestamp(time).strftime('%a, %b %d'):<8} "
        min = daily['temperature_2m_min'][i]
        max = daily['temperature_2m_max'][i]
        code = weather_codes[daily['weathercode'][i]][1]
        answer += f"{code}{round((min+max)/2):>4}°C\n"

    answer += '`'

    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN
    )


def whoami(update, context):
    extension = random.choice(who[2]) if random.randrange(3) == 2 else ''

    name = extension['0'] + ' ' if '0' in extension else ''
    name += random.choice(who[0]) + ' ' + random.choice(who[1])
    name += ' ' + extension['1'] if '1' in extension else ''

    id = update.message.from_user.id
    context.chat_data['users'][id]['name'] = name

    username = context.chat_data['users'][id]['username']
    update.message.reply_text(f"{username}, вы — {name}", quote=False)


def whois(update, context):
    who = re.sub(f"{BOT_NAME}.*кто", "", update.message.text, flags=re.I)
    who = who.replace('?', '').strip().lower()
    id = random.choice(list(context.chat_data['users'].keys()))
    name = context.chat_data['users'][id]['username']
    who = f"{random.choice(who_quotes)} {who} - ".capitalize() + name
    update.message.reply_text(who, quote=False)


def wisdom(update, context):
    query = re.sub(
        f"{BOT_NAME}.*мудрость", "", update.message.text, flags=re.I)
    answer = query + " " + balaboba(query, 11)
    update.message.reply_text(answer)


def wiki(update, context):
    query = re.sub(
        f"{BOT_NAME}.*что такое", "", update.message.text, flags=re.I)
    answer = query + balaboba(query, 8)
    update.message.reply_text(answer)


def names(update, context):
    answer = ''
    for user, data in context.chat_data['users'].items():
        if 'name' in data and data['name']:
            if 'username' in data:
                answer += f"*{data['username'].strip('@')}* - {data['name']}\n"
    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN)


def quiz(update, context):
    for job in context.job_queue.jobs():
        if job.name == "quiz" + str(update.effective_message.chat_id):
            return

    con = sqlite3.connect("quiz.db")
    cur = con.cursor()

    res = cur.execute("select * from questions order by random() limit 1")
    row = res.fetchone()
    question = row[0]
    answers = row[1].split(',')
    correct_answer = row[2]

    answers.append(correct_answer)
    random.shuffle(answers)
    correct_index = answers.index(correct_answer) + 1

    reply = f"{question}\n\n"

    buttons = []
    keyboard = []

    longest_answer = len(sorted(answers, key=len, reverse=True)[0])
    for i, a in enumerate(answers):
        buttons.append(
            InlineKeyboardButton(
                a.strip(), callback_data=str(i + 1)+','+a.strip()
            )
        )
        if i % 2 == 1 or longest_answer > 15:
            keyboard.append(buttons)
            buttons = []

    reply_markup = InlineKeyboardMarkup(keyboard)

    con.close()

    chat_id = update.effective_message.chat_id

    remove_job_if_exists("quiz" + str(chat_id), context)

    message = update.message.reply_text(
        reply, quote=False, reply_markup=reply_markup
    )

    data = {
        'chat_id': chat_id,
        'message_id': message.message_id,
        'correct_answer': correct_answer,
        'correct_index': correct_index,
        'context': context,
        'question': question
    }

    context.job_queue.run_once(
        quiz_finish, 10, name="quiz" + str(chat_id), context=data
    )


def quiz_answer(update, context):
    query = update.callback_query
    query.answer()
    for job in context.job_queue.jobs():
        if job.name == "quiz" + str(update.effective_message.chat_id):
            if "quiz" not in job.context:
                job.context["quiz"] = {}
            job.context["quiz"][query.from_user.id] = query.data
            break


def quiz_finish(context):
    job = context.job.context

    correct_answer = job["correct_answer"]
    correct_index = job["correct_index"]
    question = job["question"]
    chat_id = job["chat_id"]
    users = job["context"].chat_data["users"]

    reply = f"{question}\n\nПравильный ответ: {correct_answer}\n\n"

    if "quiz" in job:
        for id, value in job["quiz"].items():
            if "quiz" not in users[id]:
                users[id]["quiz"] = {"answers": 0, "correct": 0}

            users[id]["quiz"]["answers"] += 1
            if int(value.split(',')[0]) == correct_index:
                result = "правильно"
                users[id]["quiz"]["correct"] += 1
            else:
                result = f"неправильно ({value.split(',')[1]})"

            username = users[id]['username'].strip('@')
            reply += f"{username} ответил {result}\n"

    context.bot.edit_message_text(
        chat_id=chat_id, message_id=job["message_id"], text=reply
    )


def quiztop(update, context):
    users = context.chat_data['users'].items()
    filtered = list(filter(lambda x: 'quiz' in x[1], users))
    sorted_data = sorted(
        filtered,
        key=lambda x: x[1]['quiz']['correct']/x[1]['quiz']['answers'],
        reverse=True
    )
    answer = 'Статистика ответов:\n\n'
    for i, (user, data) in enumerate(sorted_data):
        correct = data['quiz']['correct']
        answers = data['quiz']['answers']
        username = data['username'].strip('@')
        answer += f"{i+1}) {username}: "
        answer += f"{correct} / {answers} "
        answer += f"({round(correct/answers*100)}%)\n"
    update.message.reply_text(answer, quote=False)
