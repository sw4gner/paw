import re
import tele_util, lst, config, roll
import time
import random
import requests
import json

REX_ZTT_ADD='\/zitat((.*)~\|~\s?(.*))?'
REX_ZTT='\/zitat\s(.*)?'

def zitat(msg):
    m = re.search(REX_ZTT_ADD, msg.upd["message"]["text"])
    if m.group(1) != None:
        sql = '''
        INSERT INTO ztt (chat_id, autor, text, cts)
        value (%(chat_id)s, %(at)s, %(tx)s, %(cts)s)
        '''
        data = {'chat_id': msg.getChatId(), 'at': m.group(3),'tx': m.group(2), 'cts': time.strftime('%Y-%m-%d %H:%M:%S')}
        tele_util.executeSQL(sql, data)
        msg.send(('%s ~|~ %s' % (m.group(2), m.group(3))))
        return "OK"
    m = re.search(REX_ZTT, msg.upd["message"]["text"])
    if m != None:
        sql = """
        select concat(text, ' ~|~ ', autor)
        from ztt
        where chat_id=%(id)s
        and lower(text) like '%%%(t)s%%'
        or lower(autor) like '%%%(t)s%%'
        order by rand() limit 1
        """ % {'id': msg.getChatId(), 't': m.group(1).lower()}
        print(sql)
        msg.send(tele_util.getOneSQL(sql))
    else:
        sql = """
        select concat(text, ' ~|~ ', autor)
        from ztt
        where chat_id=%s order by rand() limit 1""" % (msg.getChatId())
        msg.send(tele_util.getOneSQL(sql))

REX_LIST='/list\s(del|rnd|)\s*(\S*)\s*(.*)?'
def list_(msg):
    m = re.search(REX_LIST, msg.upd["message"]["text"])
    if m == None:
        ls = lst.getAllLists(msg.getChatId())
        msg.send(('*All*\n%s' % (lst.prtList(ls))), parse_mode='Markdown')
        return
    else:
        modus = m.group(1)
        name = m.group(2)
        entry = m.group(3)
        if len(modus) == 0 and len(entry) > 0:
            lst.addList(msg.getChatId(), name, entry)
        elif modus == 'del':
            lst.delList(msg.getChatId(), name, entry)
        elif modus == 'rnd':
            msg.send('*Random %s:* = %s' % (name, lst.rndList(msg.getChatId(), name)), parse_mode='Markdown')
            return
        ls = lst.getList(msg.getChatId(), name)
        msg.send(('*%s:*\n[%s]' % (name, lst.prtList(ls))), parse_mode='Markdown')

rol_dec = {}
def roulette(msg):
    global rol_dec
    val = None
    if msg.getChatId() in rol_dec:
        t, val = rol_dec[msg.getChatId()]
        if time.strftime('%Y-%m-%d') != t:
            val = None
    if val == None:
        val = lst.rndList(msg.getChatId(), 'roulette')
        rol_dec[msg.getChatId()]=(time.strftime('%Y-%m-%d'), val)
    msg.send('*%s* hat /roulette am %s gewonnen!' % (val, time.strftime('%Y-%m-%d')), parse_mode='Markdown')
    url = getGiphy(val)
    if url:
        msg.send(url, typ='d')


def bit(msg):
    if random.randint(0,100) >= 40:
        msg.send('CgADBAADaAADDOAFUX2bfkqLEdVSFgQ', typ='d') # No
    else:
        msg.send('CgADBAADyJIAAhwXZAfKFg_xUcgLxRYE', typ='d') # Yes

def gif(msg):
    url = getGiphy(msg.txt)
    if url == None:
        default=tele_util.getProp(msg.getChatId(), 'tenor/default', default='otter')
        url = getGiphy(default)
    msg.send(url, typ='d', reply=True)

def tenor(msg):
    url = getTenor(msg.txt)
    if url == None:
        default=tele_util.getProp(msg.getChatId(), 'tenor/default', default='sexy')
        url = getTenor(default)
    msg.send(url, typ='d', reply=True)

def getGiphy(term):
    r = requests.get("http://api.giphy.com/v1/gifs/search?lang=de&api_key=%s&q=%s&rating=R&limit=1&offset=%s" \
                     % (config.apikeys['giphy'], term, random.randint(1,10)))
    if r.status_code == 200:
        jobj = json.loads(r.content)
        if 'data' in jobj and len(jobj['data'])>0:
            return jobj['data'][0]['images']["original"]["url"].replace('\/', '/')

def getTenor(term):
    r = requests.get("https://api.tenor.com/v1/random?key=%s&limit=1&q=%s&locale=de_GER" \
                     % (config.apikeys['tenor'], term))
    if r.status_code == 200:
        jobj = json.loads(r.content)
        if 'results' in jobj and len(jobj['results'])>0:
            return jobj['results'][0]["url"]

def rollFunc(msg):
    _, roll_text = roll.roll(msg.txt)
    msg.send(roll_text, parse_mode='Markdown')

def dailyPost(msg):
    tags=tele_util.getProp(msg.getChatId(), 'dayliePost/tags', default='r/otters')
    typ3, msg_txt = getDailyPost(tags)
    msg.send(msg_txt, typ=typ3)

@tele_util.onceADay
def getDailyPost(tags):
    sql = "select id, file_id, type from daylie_post where tags like '%s' and date_day='%s' limit 1" \
            % (tags, time.strftime('%Y-%m-%d'))
    rows = tele_util.readSQL(sql)
    if rows:
        return rows[0][2], rows[0][1]
    else:
        sql = """ select id, file_id, type from daylie_post where tags like '%s' and date_day=''
        order by rand() limit 1""" % (tags)
        rows = tele_util.readSQL(sql)
        sql = "update daylie_post set date_day = '%s' where id=%s" % (time.strftime('%Y-%m-%d'), rows[0][0])
        tele_util.executeSQL(sql)
        return rows[0][2], rows[0][1]


REX_MSG='\/svb (-?\d*) (.*)'
@tele_util.onlySysUser
def sendViaBot(msg):
    m = re.search(REX_MSG,msg.upd["message"]["text"])
    if m == None:
        return "OK"
    msg.bot.sendMessage(m.group(1), m.group(2))





