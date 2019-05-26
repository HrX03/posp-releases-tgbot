import requests
import json
from datetime import datetime
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import logging
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.environ['token']

updater = Updater(token)
dispatcher = updater.dispatcher

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("Don't even try it".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = re.sub("'", "", str(self.rfile.read(content_length)).replace("b", ""))

        print(post_data)

        if post_data.startswith("device="[0:7]):
            new_update = checkUpdates("New update available", post_data.replace("device=", ""))
            if not (new_update.startswith("No updates found for device")):
                #params = (
                #    ('chat_id', -1001270384479),
                #    ('text', new_update),
                #    ('parse_mode', "Markdown"),
                #    ('disable_web_page_preview', "yes")
                #)

                #requests.post("https://api.telegram.org/bot" + token + "/sendMessage", params=params)

                self.wfile.write(new_update.encode('utf-8'))
            else:
                self.wfile.write("Unknown device.".encode('utf-8'))
        else:
            return

def latest(bot, update):
    try:
        device = (update.message.text).split(" ")[1]
    except IndexError:
        device = None

    if not (device is None):
        bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=checkUpdates("Latest update", device))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Device can't be empty.\nUsage: /latest <device>")

def checkUpdates(update_string, device):
    payload = {'device': device, 'type': 'weekly'}
    r = requests.get("https://api.potatoproject.co/checkUpdate", params=payload)

    try:
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

def sendUpdateMessageToChannel(bot, update):
    -1001467812943

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

latest_handler = CommandHandler('latest', latest)
dispatcher.add_handler(latest_handler)

updater.start_polling()

run()