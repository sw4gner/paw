#!/usr/bin/python3.6

from flask import Flask, request
import config

from poll import createNew, closePoll, updatePoll, getPoll
from timer import timer_html
from roll import roll
from quotes import toggleSub

bot = config.bot

dnbot = None

app = Flask(__name__)

@app.route(config.swagbot['hook'], methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if 'callback_query' in update:
        updatePoll(update)
        return "OK"
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        if update["message"]["text"].startswith('/roll '):
            roll_val, roll_msg = roll(update["message"]["text"][6:], [])
            bot.sendMessage(chat_id, ''.join(roll_msg), parse_mode='Markdown')
            return "OK"
        if update["message"]["text"].startswith('/togglesub'):
            text = toggleSub(update)
            bot.sendMessage(chat_id, text, parse_mode='Markdown')
            return "OK"
        if update["message"]["text"].startswith('/poll '):
            createNew(update)
            return "OK"
        if update["message"]["text"] == '/closepoll':
            poll = getPoll(chat_id)
            if poll != None:
                closePoll(poll)
            return "OK"
    return "OK"

@app.route(config.dntelegram['hook'], methods=['POST'])
def dnidb():
    update = request.get_json()
    chat_id = update["message"]["chat"]["id"]
    dnbot.sendMessage(chat_id, "Coming soon!", parse_mode='Markdown')
    return "OK"

@app.route('/timer.html', methods=['GET'])
def timer():
    return timer_html
