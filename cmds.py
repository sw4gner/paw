import re
import tele_util, lst, config, roll
import time
import random
import requests
import json
import html

REX_ZTT_ADD='\/zitat((.+)~\|~\s?(.*))?'
REX_ZTT='\/zitat[^@](.*)?'

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

def quiz (msg):
    sql = "select text, autor from ztt where chat_id=%s and text <> '' order by rand() limit 1"
    text, autor = tele_util.readSQL(sql, data=[str(msg.getChatId())])[0]
    sql = "select autor from ztt where chat_id=%s and autor!=%s and text<>'' group by autor order by rand() limit 5"
    r = tele_util.readSQL(sql, data=[str(msg.getChatId()), autor])
    a = [e[0] for e in r]
    a.append(autor)
    random.shuffle(a)
    url = 'https://api.telegram.org/bot%s/sendpoll' % config.swagbot['api_key']
    myobj = {'chat_id': msg.getChatId(), 'question': text, 'options': a, 'correct_option_id':a.index(autor), 'type': 'quiz', 'is_anonymous':False}
    requests.post(url, json = myobj)

def trivia(msg, config=config.swagbot):
    url = 'https://opentdb.com/api.php?amount=1&type=multiple'
    rs = requests.get(url).json()['results'][0]
    options = rs['incorrect_answers'] + [rs['correct_answer']]
    random.shuffle(options)
    url = 'https://api.telegram.org/bot%s/sendpoll' % config['api_key']
    myobj = {'chat_id': msg.getChatId(), 'question': html.unescape(rs['question']), 'options': [html.unescape(e) for e in options], 'correct_option_id':options.index(rs['correct_answer']), 'type': 'quiz', 'is_anonymous':False}
    requests.post(url, json = myobj)

REX_LIST='/list\s(del|rnd|)\s*(\S*)\s*(.*)?'
def list_(msg):
    m = re.search(REX_LIST, msg.upd["message"]["text"])
    if m == None:
        ls = lst.getAllLists(msg.getChatId())
        msg.send('*Alle:*\n%s' % (lst.prtList(ls)), parse_mode='Markdown')
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
            msg.send('*Random %s* = %s' % (name, lst.rndList(msg.getChatId(), name)), parse_mode='Markdown')
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
    if random.randint(0,100) <= 40:
        msg.send('CgADBAADaAADDOAFUX2bfkqLEdVSFgQ', typ='d') # No
    else:
        msg.send('CgADBAADyJIAAhwXZAfKFg_xUcgLxRYE', typ='d') # Yes

def gif(msg):
    url = getGiphy(msg.txt)
    if url == None:
        default=tele_util.getProp(msg.getChatId(), 'gif/default', default='otter')
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
    tags=tele_util.getProp(msg.getChatId(), 'dayliePost/tags', default='r/bikinis')
    typ3, msg_txt = getDailyPost(tags)
    msg.send(msg_txt, typ=typ3, caption=time.strftime('%Y-%m-%d'))

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
        if len(rows) == 0:
            return 'der tag '+tags+' ist aufgebraucht', 'm'
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

REX_PROP='(\S*)\s*(.*)'
@tele_util.onlySysUser
def props(msg):
    m = re.search(REX_PROP,msg.txt)
    if m == None:
        return
    data = {'chat_id': str(msg.getChatId()), 'name': m.group(1),'value': m.group(2)}
    sql = "select value from props where chat_id=%(chat_id)s and name=%(name)s"
    value = tele_util.getOneSQL(sql, data=data)
    if value:
        sql = "update props set value=%(value)s where chat_id=%(chat_id)s and name=%(name)s"
        tele_util.executeSQL(sql, data=data)
    else:
        value='None'
        sql = "insert into props (chat_id, name, value) values (%(chat_id)s, %(name)s, %(value)s)"
        tele_util.executeSQL(sql, data=data)
    tele_util.clearGetProp()
    newval=str(tele_util.getProp(msg.getChatId(), m.group(1)))
    msg.send('Property *'+m.group(1)+'* von *'+value+'* nach *'+newval+'* geändert', parse_mode='Markdown')

def truth(msg):
    if random.randint(0,100) >= int(tele_util.getProp(msg.getChatId(), 'dareortruth/perc', default=34)):
        user = lst.rndList(msg.getChatId(), 'truthordare') or 'benutze /list truthordare um Optionen hinzuzufügen'
    else:
        user = 'du selber'
    text = tele_util.getOneSQL("select text from tod where type in ("+tele_util.getProp(msg.getChatId(), 'dareortruth/types', default="'t','r','n','m','i'")+") order by rand() limit 1")
    msg.send(user+' truth:\n'+text);
def dare(msg):
    if random.randint(0,100) >= int(tele_util.getProp(msg.getChatId(), 'dareortruth/perc', default=34)):
        user = lst.rndList(msg.getChatId(), 'truthordare') or 'benutze /list truthordare um Optionen hinzuzufügen'
    else:
        user = 'du selber'
    text = tele_util.getOneSQL("select text from tod where type='d' order by rand() limit 1")
    msg.send(user+' dare:\n'+text)

def stats(msg):
    msg.send([sum(e)-min(e) for e in [[random.randint(1,6) for i in range(4)] for n in range(6)]])

def inspirobot(msg):
    url='https://inspirobot.me/api?generate=true'

