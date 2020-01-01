'''
utility to work with telepot api

@author: swagner
'''
import re
import telepot
import MySQLdb
import config
import time
from contextlib import closing
from functools import lru_cache

###############################################################################
###### decorators #############################################################

def onlySysUser(func):
    def wrap(*args):
        msg =args[0]
        if msg.getUser() in config.sysuser:
            return func(*args)
        else:
            return None
    return wrap

def catchKeyError (func):
    '''
    decorator to catch KeyError and return None
    '''
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return None
    return wrap

oadCache={}
oadDate=''
def onceADay(fnc):
    def wrapper(*args):
        global oadCache
        global oadDate
        if not time.strftime('%Y%m%d') in oadDate:
            oadCache={}
            oadDate=time.strftime('%Y%m%d')
        if not oadCache.get(str(args)):
            oadCache[str(args)] = fnc(*args)
        return oadCache.get(str(args))
    return wrapper
###### decorators #############################################################
###############################################################################
@onceADay
def f(a):
    print (a)
    return a

class MsgUtil(object):
    '''
    warper for telgram update
    '''
    def __init__(self, bot, upd):
        self.bot=bot
        self.upd=upd
        self.TXT_PATT='\/(\w*)(?>@%s)?\s?(.*)?' % bot.getMe()['username']
        self.cmd, self.txt  = self.paseText(upd)

    def paseText(self, upd):
        if 'text' not in upd['message']:
            return (None, None)
        m = re.search(self.TXT_PATT, upd["message"]["text"])
        if m == None:
            return (None, None)
        elif len(m.group(2)) > 0:
            return (m.group(1),m.group(2))
        else:
            return (m.group(1), None)

    def getChatId(self):
        return self.upd["message"]["chat"]["id"]
        
    def send (self, msg_txt, typ='m', parse_mode=None, reply=False, caption=None):
        kwargs = {}
        if caption:
            kwargs['caption'] = caption
        if parse_mode:
            kwargs['parse_mode'] = parse_mode
        if typ == 'm':
            self.bot.sendMessage(self.getChatId, msg_txt, **kwargs)
        if type == 'd':
            self.bot.sendDocument(self.getChatId, msg_txt, **kwargs)
    @catchKeyError
    def getUser(self):
        '''
        :return: message>from>id
        '''
        return self.upd["message"]["from"]["id"]


###############################################################################
### DB                                     ###################################

@lru_cache(maxsize=10)
def getProp(chat, name, default=None):
    sql = "select value from props where chat_id='%s' and name='%s'" % (chat, name)
    return getOneSQL(sql) or default
    
def getCon():
    return MySQLdb.connect(config.con_info)

def executeSQL(sql, data=None, cnt=0):
    with closing(getCon()) as con:
        with closing(con.cursor()) as cur:
            if data == None:
                rscnt = cur.execute(sql)
            else:
                rscnt = cur.execute(sql,data)
            if cnt == 0 or rscnt == cnt:
                con.commit()

def getOneSQL(sql, data=None):
    ret = readSQL(sql, data)
    if not ret:
        return None
    else:
        return ret[0][0]
    
def readSQL(sql, data=None):
    with closing(getCon()) as con:
        with closing(con.cursor()) as cur:
            if data == None:
                cur.execute(sql)
            else:
                cur.execute(sql,data)
            return cur.fetchall() or None

### DB                                     ###################################
###############################################################################

def startBot(conf):
    bot = telepot.Bot(conf['api_key'])
    bot.setWebhook(config.site+conf['hook'], max_connections=1)
    return bot

@onlySysUser
@catchKeyError
def addFile(msg):
    upd=msg.upd
    if 'photo' in upd['message']:
        addPhoto(upd['message']['photo'][0]['file_id'], 'p')
    if 'animation' in upd['message']:
        addPhoto(upd['message']['animation']['file_id'], 'g')
    return "OK"

def addPhoto (file_id, typ3):
    sql = '''
    INSERT INTO daylie_post (file_id, type, date_day,tags, cts)
    SELECT '%(f)s', '%(t)s', '', 'b', '%(ts)s' FROM DUAL WHERE NOT EXISTS (
        SELECT file_id FROM daylie_post WHERE file_id = '%(f)s'
    ) LIMIT 1'''
    data = {'f':file_id, 't': typ3, 'ts': time.strftime('%Y-%m-%d %H:%M:%S')}
    executeSQL(sql, data)