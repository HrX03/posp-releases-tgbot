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
        update.message.reply_markdown(checkUpdates("Latest update", device, 'weekly'), disable_web_page_preview=True)
    else:
        update.message.reply_markdown("Device can't be empty.\nUsage: /latest <device>")

def mashed(bot, update):
    if update.message.chat_id == -1001304020599:
        return

    try:
        device = (update.message.text).split(" ")[1]
    except IndexError:
        device = None

    if not (device is None):
        update.message.reply_markdown(checkUpdates("WARNING: Mashed builds are highly experimental and can even make your phone not turn on anymore. Please know what are you doing before flashing them.\n\nLatest mashed update", device, 'mashed'), disable_web_page_preview=True)
    else:
        update.message.reply_markdown("Device can't be empty.\nUsage: /latest <device>")

def changelog(bot, update):
    cl_text = requests.get("https://raw.githubusercontent.com/PotatoProject/vendor_potato/baked-release/CHANGELOG.md").text.replace("# Changelog\n", "")
    cl_array = cl_text.split("\n\n### ")

    update.message.reply_text("Latest release changelog:\n" + cl_array[1])

def checkUpdates(update_string, device, type):
    payload = {'device': device, 'type': type}

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
            "\n    *Maintainer:* " + parse_maintainer(device) + 
            "\n    *Date of upload:* " + datetime.utcfromtimestamp(posp_standard_json['datetime']).strftime('%Y-%m-%d') +
            "\n    *Size:* " + str(posp_standard_json['size'])[0:3] + "MB" +
            "\n    *Release type:* " + posp_standard_json['romtype'])
    else:
        if type == "mashed":
            return "No mashed builds found for device " + device
        else:
            return "No updates found for device " + device

def devices(bot, update):
    devices = requests.get("https://raw.githubusercontent.com/PotatoProject/vendor_potato/baked-release/potato.devices").text
    devices_array = devices.split('\n')
    print(devices_array)

    update.message.reply_markdown("Complete list of *official* devices:\n    " + "\n    ".join(devices_array))

def parse_maintainer(device):
    if device == "bacon":
        return "Kshitij Gupta (fancypants)"
    elif device == "beryllium":
        return "Kshitij Gupta (fancypants)"
    elif device == "cheeseburger":
        return "Spherical Flying Kat (SphericalKat)"
    elif device == "chiron":
        return "HrX03 (HrX03)"
    elif device == "dipper":
        return "Argraur (argraur)"
    elif device == "enchilada":
        return "Samriddha Basu (TheDorkKnightRises)"
    elif device == "fajita":
        return "Ujwal (Raidenv1)"
    elif device == "kenzo":
        return "Absar Rahman (adolfthereaper)"
    elif device == "mido":
        return "Rahul (beingmishra)"
    elif device == "oneplus2":
        return "Shreyansh Lodha (ShreyanshLodha)"
    elif device == "oneplus3":
        return "Jagrav Naik (Jagrav Naik)"
    elif device == "onyx":
        return "Kushagra Vipradas (warmachine98)"
    elif device == "potter":
        return "Ashwin R C (AshwinRC)"
    elif device == "sagit":
        return "dpatrongomez (dpatrongomez)"
    elif device == "sanders":
        return "Dybios (Dybios)"
    elif device == "santoni":
        return "Zainudin Shamilov (ErrorNetwork28)"
    elif device == "tissot":
        return "Keian (keikei14)"
    elif device == "vince":
        return "4PERTURE (probuildbot)"
    elif device == "whyred":
        return "rajadeja (jadejaraj)"
    elif device == "X00T":
        return "Yami Sukehiro (BabluS)"
    elif device == "zenfone3":
        return "Abhay (vegeto1806)"
    else:
        return "?"

latest_handler = CommandHandler('latest', latest)
dispatcher.add_handler(latest_handler)

latest_handler = CommandHandler('mashed', mashed)
dispatcher.add_handler(latest_handler)

changelog_handler = CommandHandler('changelog', changelog)
dispatcher.add_handler(changelog_handler)

changelog_handler = CommandHandler('devices', devices)
dispatcher.add_handler(changelog_handler)

updater.start_polling()