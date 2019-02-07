#!/usr/bin/python3.6
import config
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot import message_identifier

df_options = [
#white up
u'\U0001F44D\U0001F3FB',
#black down
u'\U0001F44E\U0001F3FF',
]

bot = config.bot

polls = {}

def updatePoll(msg):
    if 'callback_query' not in msg:
        return
    chatid = msg['callback_query']['message']['chat']['id']
    poll = getPoll(chatid)
    poll['votes'][msg['callback_query']['from']['id']] = msg['callback_query']['data']
    printPoll(poll)

def closePoll(poll):
    chatid, msgid = message_identifier(poll['msgobj'])
    bot.editMessageReplyMarkup(message_identifier(poll['msgobj']), reply_markup=None)
    bot.sendMessage(chatid, 'poll geschlossen' , reply_to_message_id=msgid)
    del polls[chatid]

def getPoll(chatid):
    return polls.get(chatid)

def getMarkup(options):
    return InlineKeyboardMarkup(inline_keyboard=\
        [[InlineKeyboardButton(text=o, callback_data=o)] for o in options])

def createPoll(msg, options, title):
    markup = getMarkup(options)
    rp_msg = bot.sendMessage(msg['message']['chat']['id'], title, reply_markup=markup)
    poll = {'chatid': msg['message']['chat']['id'],
            'msgobj': rp_msg,
            'votes': {},
            'title': title,
            'options': options,}
    polls[msg['message']['chat']['id']] = poll
    return poll

def printPoll(poll):
    votes = poll['votes']
    keys = set(votes.values())
    grpd_votes = [[key, len([key for v in votes.values() if v == key])] for key in keys]
    result = '\n'.join(['%s: %s' % (g[0], ''.join(['*' for i in range(g[1])])) for g in grpd_votes])
    msg_ident = message_identifier(poll['msgobj'])
    text =  '%s:\n%s' % (poll['title'], result)
    markup = getMarkup(poll['options'])
    bot.editMessageText(msg_ident, text, reply_markup=markup)


def createNew(msg, options=None):
    title = msg['message']['text'][6:]
    chatid = msg['message']['chat']['id']
    poll = getPoll(chatid)
    if poll != None:
        closePoll(poll)
    if options == None:
        options = df_options
    poll = createPoll(msg, options, title)