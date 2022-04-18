# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable-msg=C0103
# pylint: disable-msg=C0200

#!/usr/bin/python

import sys
import time
import yaml

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from twilio.rest import Client

URL = "https://store.ui.com/collections/unifi-protect-cameras"

def log(text):
    print(time.ctime() + ' :: ' + text, flush=True)

def send_text(body, media):
    twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = twilio_client.messages.create(body=body, from_=FROM_NUM, to=TO_NUM, media_url=media)
    log("SMS Receipt: " + message.sid)

def search(lastbody):
    session = HTMLSession()
    resp = session.get(URL)
    resp.html.render()
    soup = BeautifulSoup(resp.html.html, "lxml")
    found = soup.find_all('div', {"id":"collectionApp"})
    body =''
    media = []
    items = []
    if found is None:
        return ''
    found_count = len(found)
    if found_count == 0:
        return ''
    for i in range(len(found)):
        sub = found[i].select('.grid__item')
        for j in range(len(sub)):
            txt = sub[j].select('.comProductTile__title')
            if not txt:
                continue
            txt = txt[0].get_text().strip().replace('\n', ' ')
            if not "Sold Out" in txt and not "Which UniFi Camera is Right For Me" in txt:
                items.append(txt)
        body = "\n\n".join(list(dict.fromkeys(items)))
        log(body)
    if body != lastbody:
        send_text(body, media)
    return body

#main
with open('config.yml', 'r') as file:
    conf = yaml.safe_load(file)
    TWILIO_SID = conf['twilio_sid']
    TWILIO_TOKEN = conf['twilio_token']
    FROM_NUM = conf['from_num']
    TO_NUM = conf['to_num']
    SLEEP_TIME_SECS = conf['sleep_time_secs']
lastBody = ''
while True:
    log("fetching unifi page")
    lastBody = search(lastBody)
    log("sleeping")
    time.sleep(SLEEP_TIME_SECS)
    sys.stdout.flush()
