#!/usr/bin/python3.6
from contextlib import closing
import config

bot = config.bot

def toggleSub(msg):
    with closing(config.getCon()) as con:
        id = msg['message']['chat']['id']
        r=None
        sql=None
        with closing(con.cursor()) as cur:
            cur.execute('select subed from quoteSubs where chatid=%s' % id)
            r = cur.fetchone()
        subed = False
        if r == None:
            subed = True
            sql = "insert into quoteSubs values (%s, 1)" % id
        elif r[0] == 0:
            subed = True
            sql = "update quoteSubs set subed=1 where chatid=%s" % id
        elif r[0] == 1:
            subed = False
            sql = "update quoteSubs set subed=0 where chatid=%s" % id
        with closing(con.cursor()) as cur:
            cur.execute(sql)
        con.commit()
    return 'Dein Zitateabo ist *aktiv*' if subed else 'Dein Zitateabo ist *inaktiv*'

def daylieQuote():
    with closing(config.getCon()) as con:
        text = None
        with closing(con.cursor()) as cur:
            cur.execute('select id, body, autor from quotes order by rand() limit 1')
            r = cur.fetchone()
            text = "_%s_\n%s" % (r[1], r[2])
        with closing(con.cursor()) as cur:
            cur = con.cursor()
            cur.execute("select chatid from quoteSubs where subed=1")
            for row in cur:
                bot.sendMessage(row[0], text, parse_mode='Markdown')