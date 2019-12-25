'''
utility to work with telepot api

@author: swagner
'''
import re
import telepot
import MySQLdb
import config
from contextlib import closing

class MsgUtil(object):
    '''
    classdocs
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

#decorators 

def sysUser(func):
    def wrap(*args):
        if getUser(args[0].upd) in config.sysuser:
            return func(*args)
        else:
            return None
    return wrap

def catchKeyError (func):
    '''
    decorator to catch KeyError and return None
    '''
    def wrap(*args, **kwargs):
        print(args[1])
        try:
            return func(*args, **kwargs)
        except KeyError:
            return None
    return wrap





@catchKeyError
def getUser(upd):
    '''
    :param upd: updatejson
    :return: message>from>id
    '''
    return upd["message"]["from"]["id"]

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
    return readSQL(sql, data)[0][0]
    
def readSQL(sql, data=None):
    with closing(getCon()) as con:
        with closing(con.cursor()) as cur:
            if data == None:
                cur.execute(sql)
            else:
                cur.execute(sql,data)
            return cur.fetchall()

def startBot(conf):
    bot = telepot.Bot(conf['api_key'])
    bot.setWebhook(config.site+conf['hook'], max_connections=1)
    return bot

