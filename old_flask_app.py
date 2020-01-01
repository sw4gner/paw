#!/usr/bin/python3.6

from flask import Flask, request, send_file
import config
import random
import re
import sys
import time
import os

from list import savNew, getList, getRandomList, getRandomFromList, removeFromList
from randgif import getRand, getRandTenor, getTrendTenor
from timer import timer_html
from roll import roll
from contextlib import closing


os.environ["TZ"] = "Europe/Berlin"
time.tzset()

daylie_post = ('0000-00-00', '', '')

bot = config.bot

dnbot = config.botdnbot

app = Flask(__name__)

@app.route(config.swagbot['hook'], methods=['POST'])
def telegram_webhook():
    try:
        update = request.get_json()
        updateMsgLog(update)
        if random.randint(0,80) == 0:
            bot.sendDocument(update["message"]["chat"]["id"], getRand('hallo'))
        if update["message"]["from"]["id"] == config.sysuser:
            if "message" in update and "photo" in update["message"]:
                addPhoto(update['message']['photo'][0]['file_id'], 'p')
                return "OK"
            if "message" in update and "animation" in update["message"]:
                addPhoto(update['message']['animation']['file_id'], 'g')
                return "OK"
            if update["message"]["text"].startswith('/sql '):
                sendsql(update["message"]["chat"]["id"], update["message"]["text"][5:])
                return "OK"
            if update["message"]["text"].startswith('/rs '):
                rex='\/rs (-?\d*) (.*)'
                m = re.search(rex,update["message"]["text"])
                if m == None:
                    return "OK"
                bot.sendMessage(m.group(1), m.group(2))
                return "OK"
        if not update["message"]["text"].startswith('/'):
            return "OK"
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            if update["message"]["text"].startswith('/zitat'):
                zitat(chat_id, update["message"]["text"])
            if update["message"]["text"].startswith('/roulette'):
                roulette(chat_id)
            if update["message"]["text"].startswith('/roll'):
                roll_val, roll_msg = roll(update["message"]["text"][6:], [])
                bot.sendMessage(chat_id, ''.join(roll_msg), parse_mode='Markdown')
                return "OK"
            elif update["message"]["text"].startswith('/talk '):
                bot.sendMessage(config.sysuser, str(chat_id) + ' : ' + ''.join(update["message"]["text"][6:]))
                return "OK"
            elif update["message"]["text"].startswith('/bit'):
                if random.randint(0,2) == 0:
                    bot.sendDocument(chat_id, 'CgADBAADaAADDOAFUX2bfkqLEdVSFgQ') # No
                else:
                    bot.sendDocument(chat_id, 'CgADBAADyJIAAhwXZAfKFg_xUcgLxRYE') # Yes
                return "OK"
            elif update["message"]["text"].startswith('/gif ') and len(update["message"]["text"]) > 6:
                term = ''.join(update["message"]["text"][5:])
                url = getRand(term)
                if url == None:
                    url = getRand('otter')
                bot.sendDocument(chat_id, url)
                return "OK"
            elif update["message"]["text"].startswith('/trend'):
                bot.sendDocument(chat_id, getTrendTenor())
                return "OK"
            elif update["message"]["text"].startswith('/tenor ') and len(update["message"]["text"]) > 8:
                term = ''.join(update["message"]["text"][7:])
                url = getRandTenor(term)
                if url == None:
                    url = getRandTenor('sexy')
                bot.sendDocument(chat_id, url)
                return "OK"
            elif update["message"]["text"].startswith('/list'):
                rex='\/list\s(del\s|)?(\S*)\s*(.*)?'
                m = re.search(rex,update["message"]["text"])
                if m == None:
                    return "OK"
                if  len(m.group(1)) > 0:
                    lst=removeFromList(chat_id, m.group(2), m.group(3))
                elif len(m.group(3)) > 0:
                    lst = savNew(chat_id, m.group(2),m.group(3))
                else:
                    lst = getList(chat_id, m.group(2))
                bot.sendMessage(chat_id, ('*%s:*\n[%s]' % (m.group(2), lst)), parse_mode='Markdown')
            elif update["message"]["text"].startswith('/randList'):
                rex='\/randList\s(\S*)?'
                m = re.search(rex,update["message"]["text"])
                if m == None:
                    return "OK"
                elif len(m.group(1)) > 0:
                    lst = getRandomList(chat_id, m.group(1))
                    bot.sendMessage(chat_id, ('*%s:*\n[%s]' % (m.group(1), lst)), parse_mode='Markdown')
            elif update["message"]["text"].startswith('/dailynsfw'):
                getnsfwpost(chat_id)
                return "OK"
            elif update["message"]["text"].startswith('/daily'):
                getdayliepost(chat_id)
                return "OK"
    except Exception  as e:
        print(str(e), file=sys.stderr)
        return "OK"
    return "OK"



@app.route(config.dntelegram['hook'], methods=['POST'])
def dnidb():
    m = request.get_json()
    if "message" in m and "text" in m["message"]:
        if m["message"]["text"].lower() == '/rndpic':
            rndPic(dnbot, m["message"]["chat"]["id"])
            return "OK"
        if m["message"]["text"].lower() == '/dumpphoto':
            dumpPhoto(dnbot, m["message"]["chat"]["id"])
            return "OK"
    store(m, dnbot)
    return "OK"

typ3s = {
    't': 'text',
    'a': 'animation',
    's': 'sticker',
    'p': 'photo',
    'v': 'video',
    'i': 'voice',
    'o': 'poll',
    'd': 'document',
    'c': 'comand',
}

def updateMsgLog(upd):
    reply=upd['message'].get('reply_to_message', {}).get('message_id', 0)
    length=len(upd['message'].get('text', '1'))
    typ3=next((key for key, val in typ3s.items() if upd['message'].get(val, None)), 'N')
    if typ3 == 't' and upd['message']['text'].startswith('/'):
        typ3 = 'c'
    sql = """
    insert into msglog
    (msg_id, user_id, chat_id, reply, date, time, day, len, type)
    values (%s,'%s','%s',%s,'%s','%s','%s',%s,'%s')
    """ % (upd['message']['message_id'],upd['message']['from']['id'],upd['message']['chat']['id'], reply,time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), time.strftime('%u'), length, typ3)
    execSql(sql)

def execSql(sql):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute(sql)
            con.commit()

def addPhoto (file_id, typ3):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            sql = ('''
            INSERT INTO daylie_post (file_id, type, date_day, tags, cts)
            SELECT '%(f)s', '%(t)s', '', 'b', '%(ts)s' FROM DUAL WHERE NOT EXISTS (
                SELECT file_id FROM daylie_post WHERE file_id = '%(f)s'
            ) LIMIT 1''' % {'f':file_id, 't': typ3, 'ts': time.strftime('%Y-%m-%d %H:%M:%S')})
            cur.execute(sql)
            con.commit()

def zitat(chat_id, text):
    rex='\/zitat((.*)~\|~\s?(.*))?'
    m = re.search(rex, text)
    if m.group(1) != None:
        with closing(config.getCon()) as con:
            with closing(con.cursor()) as cur:
                sql = ('''
                INSERT INTO ztt (chat_id, autor, text, cts)
                value (%(chat_id)s, '%(at)s', '%(tx)s', '%(cts)s')
                ''' % {'chat_id':chat_id, 'at': m.group(3),'tx': m.group(2), 'cts': time.strftime('%Y-%m-%d %H:%M:%S')})
                cur.execute(sql)
                con.commit()
                bot.sendMessage(chat_id, ('%s ~|~ %s' % (m.group(2), m.group(3))))
                return "OK"
    rex='\/zitat\s(.*)?'
    m = re.search(rex, text)
    if m != None:
        sql = "select 'm',concat(text, ' ~|~ ', autor) from ztt where chat_id=%s and lower(text) like '%%%s%%' or lower(autor) like '%%%s%%' order by rand() limit 1" % (chat_id, m.group(1).lower(), m.group(1).lower())
        sendsql(chat_id,sql)
    else:
        sql = "select 'm',concat(text, ' ~|~ ', autor) from ztt where chat_id=%s order by rand() limit 1" % (chat_id)
        sendsql(chat_id,sql)


def sendsql(chat_id, sql, mybot=bot):
    '''
    r[0] type p = foto, g = document, m= msg
    r[1] msg / fileid
    '''
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute(sql)
            for r in cur.fetchall():
                if r[0] == 'p':
                    mybot.sendPhoto(chat_id, r[1])
                elif r[0] == 'g':
                    mybot.sendDocument(chat_id, r[1])
                else:
                    mybot.sendMessage(chat_id, r[1])

rol_dec = {}
def roulette(chat_id):
    global rol_dec
    val = None
    if chat_id in rol_dec:
        t, val = rol_dec[chat_id]
        if time.strftime('%Y-%m-%d') != t:
            val = None
    if val == None:
        val = getRandomFromList(chat_id, 'roulette')
        rol_dec[chat_id]=(time.strftime('%Y-%m-%d'), val)
    bot.sendMessage(chat_id, '*%s* hat /roulette am %s gewonnen!' % (val, time.strftime('%Y-%m-%d')), parse_mode='Markdown')
    bot.sendDocument(chat_id, getRand(val))
    return "OK"


nsfw_post = ('0000-00-00', '', '')

def getnsfwpost(chat_id):
    global nsfw_post
    t, fileId, typ3 = nsfw_post
    if time.strftime('%Y-%m-%d') != t:
        with closing(config.getCon()) as con:
            with closing(con.cursor()) as cur:
                cur.execute("select id, file_id, type from daylie_post where tags in ('r/stripgirls', 'r/sexygirls') and date_day='%s'" % time.strftime('%Y-%m-%d'))
                r = cur.fetchone()
                if r == None:
                    cur.execute("select id, file_id, type from daylie_post where tags in ('r/stripgirls', 'r/sexygirls') and date_day='' order by rand() limit 1")
                    r = cur.fetchone()
                    if r == None:
                        bot.sendMessage(chat_id, '*Bitte auffüllen :-(*', parse_mode='Markdown')
                        return
                nsfw_post = (time.strftime('%Y-%m-%d'), r[1], r[2])
                with closing(con.cursor()) as cur2:
                    cur2.execute("update daylie_post set date_day = '%s' where id=%s" % (time.strftime('%Y-%m-%d'), r[0]))
                    con.commit()
            t, fileId, typ3 = nsfw_post
    if typ3 == 'p':
        bot.sendPhoto(chat_id, fileId, caption=u'\U0001F608\U0001F4A6\U0001F30B')
    else:
        bot.sendDocument(chat_id, fileId, caption=u'\U0001F608\U0001F4A6\U0001F30B')

def getdayliepost(chat_id):
    global daylie_post
    t, fileId, typ3 = daylie_post
    if time.strftime('%Y-%m-%d') != t:
        with closing(config.getCon()) as con:
            with closing(con.cursor()) as cur:
                cur.execute("select id, file_id, type from daylie_post where tags='r/otters' and date_day='%s'" % time.strftime('%Y-%m-%d'))
                r = cur.fetchone()
                if r == None:
                    cur.execute("select id, file_id, type from daylie_post where tags='r/otters' and date_day='' order by rand() limit 1")
                    r = cur.fetchone()
                    if r == None:
                        bot.sendMessage(chat_id, '*Bitte auffüllen :-(*', parse_mode='Markdown')
                        return
                daylie_post = (time.strftime('%Y-%m-%d'), r[1], r[2])
                with closing(con.cursor()) as cur2:
                    cur2.execute("update daylie_post set date_day = '%s' where id=%s" % (time.strftime('%Y-%m-%d'), r[0]))
                    con.commit()
            t, fileId, typ3 = daylie_post
    if typ3 == 'p':
        bot.sendPhoto(chat_id, fileId, caption=u'\U0001F9A6\U0001F9A6\U0001F9A6')
    else:
        bot.sendDocument(chat_id, fileId, caption=u'\U0001F9A6\U0001F9A6\U0001F9A6')
    #bot.sendDocument(chat_id,'CgADBAAD7gEAAnNK_FEzhF6_uX7faRYE')

def dumpPhoto(bot, chat_id):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute('select file_id from photo limit 100')
            for r in cur.fetchall():
                bot.sendPhoto(chat_id, r[0], caption=r[0])

def rndPic(bot, chat_id):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute('select file_id from photo order by rand() limit 1')
            r = cur.fetchone()
            bot.sendPhoto(chat_id, r[0])

def store (m, bot):
    if 'message' in m and 'photo' in m['message'] and 'file_id' in m['message']['photo'][0]:
        file_id = m['message']['photo'][0]['file_id']
        with closing(config.getCon()) as con:
            with closing(con.cursor()) as cur:
                cur.execute("select file_id from photo where file_id='%s'" % file_id)
                r = cur.fetchone()
            if r == None:
                with closing(con.cursor()) as cur:
                    cur.execute("insert into photo values ('%s')" % file_id)
                chat_id = m["message"]["chat"]["id"]
                bot.sendMessage(chat_id, 'Thanks, your contact information will be sent to the authorities.', parse_mode='Markdown')
            else:
                print('no insert')
            con.commit()

def tryAndLogError(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception  as e:
            print(str(e), file=sys.stderr)
            return "OK"
    return wrapper

@app.route('/timer.html', methods=['GET'])
def timer():
    return timer_html

@app.route('/silence.png')
def hello_world():
    text = request.args.get('text')
    createOutPng(text)
    return send_file("/home/fia4awagner/mysite/img/out.png", attachment_filename='silence.png',mimetype='image/png')

crabbot = config.crabbot

@app.route(config.crabtelegram['hook'], methods=['POST'])
@tryAndLogError
def crabhook():
    m = request.get_json()
    if "message" in m and "text" in m["message"] and m["message"]["text"].startswith('/silence'):
        createOutPng(m["message"]["text"][9:])
        with open("/home/fia4awagner/mysite/img/out.png", "rb") as f:
            crabbot.sendPhoto(m["message"]["chat"]["id"], ('silence.png', f))
    return "OK"

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
font = ImageFont.truetype("/home/fia4awagner/mysite/img/20db.otf", 25)
def createOutPng(text):
    with Image.open("/home/fia4awagner/mysite/img/silence.png") as img:
        draw = ImageDraw.Draw(img)
        draw.text((22, 35), text ,(255,255,255),font=font)
        img.save('/home/fia4awagner/mysite/img/out.png')


oadCache=[]
oadDate=''
def onceADay(fnc):
    def wrapper(*args):
        global oadCache
        global oadDate
        if not time.strftime('%Y%m%d') in oadDate:
            oadCache=[]
            oadDate=time.strftime('%Y%m%d')
        if (str(args)) in oadCache:
            return True
        else:
            oadCache.append(str(args))
            return fnc(*args)
    return wrapper

@onceADay
def syncUser(chat_id):
    sql = "select user_id from msglog where chat_id='%s' group by user_id;" % (chat_id)
    for user in readSql(sql):
       user = bot.getChatMember(chat_id, user[0])['user']
       for i in ['user_id','first_name','username','last_name']:
           if not user.get(i):
               user[i] = ''
       sql = "delete from usr where user_id='%(id)s';" % user
       execSql(sql)
       sql = "insert into usr (user_id,first_name,username,last_name) values ('%(id)s','%(first_name)s','%(username)s','%(last_name)s');" % user
       execSql(sql)

def readSql(sql):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute(sql)
            return cur.fetchall()