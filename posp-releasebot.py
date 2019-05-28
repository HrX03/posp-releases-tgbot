import requests
import json
from datetime import datetime
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import logging
import socketserver
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.environ['token']

updater = Updater(token)
dispatcher = updater.dispatcher

def latest(bot, update):
    try:
        device = (update.message.text).split(" ")[1]
    except IndexError:
        device = None

    if not (device is None):
        bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=checkUpdates("Latest update", device))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Device can't be empty.\nUsage: /latest <device>")

def changelog(bot, update):
    cl_text = requests.get("https://raw.githubusercontent.com/PotatoProject/vendor_potato/baked-release/CHANGELOG.md").text.replace("# Changelog\n", "")
    cl_array = cl_text.split("\n\n### ")

    bot.send_message(chat_id=update.message.chat_id, text="Latest release changelog:\n" + cl_array[1])

def checkUpdates(update_string, device):
    payload = {'device': device, 'type': 'weekly'}

    try:
        r = requests.get("https://api.potatoproject.co/checkUpdate", params=payload)
        posp_standard_json = r.json()['response'][-1]
    except ConnectionError:
        r = requests.get("http://api.strangebits.co.in/checkUpdate", params=payload, verify=False)
        posp_standard_json = r.json()['response'][-1]
    except IndexError:
        r = None

    if not (r is None):
        return (update_string + " for device " + device + ":" +
            "\n    *Download URL:* " + "[Get the update here!](" + posp_standard_json['url'] + ")" + 
            "\n    *Version:* " + posp_standard_json['version'] + 
            "\n    *Date of upload:* " + datetime.utcfromtimestamp(posp_standard_json['datetime']).strftime('%Y-%m-%d') +
            "\n    *Size in megabytes:* " + str(posp_standard_json['size'])[0:3] + "MB" +
            "\n    *Release type:* " + posp_standard_json['romtype'])
    else:
        return "No updates found for device " + device

latest_handler = CommandHandler('latest', latest)
dispatcher.add_handler(latest_handler)

changelog_handler = CommandHandler('changelog', changelog)
dispatcher.add_handler(changelog_handler)

updater.start_polling()