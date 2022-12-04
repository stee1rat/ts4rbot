import json
import re
import urllib.request

from fake_headers import Headers
from settings import BOT_NAME
from telegram.ext import Filters, MessageHandler


def balaboba(query, intro):
    headers = Headers().generate()
    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": query, "intro": intro, "filter": 1}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode('utf8'))['text']


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def getMessageHandler(cmd, func, sync=False):
    return MessageHandler(
        Filters.regex(re.compile(f"(?i)({BOT_NAME}.*{cmd}.*)", re.IGNORECASE)),
        func,
        sync)
