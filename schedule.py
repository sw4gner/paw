#!/usr/bin/python3.6
from datetime import date, datetime
import holidays
import config
import tele_util
import lst


swagbot = tele_util.startBot(config.swagbot)

if date.today() in holidays.DE(years=date.today().year):
    sql = "select chat_id from props where name='holidays'"
    rows = tele_util.readSQLL(sql)
    for r in rows:
        swagbot.sendMessage(r[0], 'Heute haben wir frei => *'+u'\U0001F389'+holidays.DE(years=2020)[date.today()]+'*'+u'\U0001F389', parse_mode='Markdown')

sql = "select chat_id, value from props where name='backlog/reminder'"
rows = tele_util.readSQL(sql)
doy = datetime.now().timetuple().tm_yday
for r in rows:
    if doy % int(r[1]) == 0:
        l=lst.getList(r[0], 'backlog')
        if len(l)>0:
            swagbot.sendMessage(r[0],('Es steht folgendes aus: %s' % l))