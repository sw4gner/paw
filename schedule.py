#!/usr/bin/python3.6
from quotes import daylieQuote
from datetime import date
import holidays
import config
from contextlib import closing


daylieQuote()

if date.today() in holidays.DE(years=date.today().year):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute("select chatid from quoteSubs where datesub=1")
            for r in cur.fetchall():
                config.bot.sendMessage(r[0], 'Heute haben wir frei => *'+u'\U0001F389'+holidays.DE(years=2020)[date.today()]+'*'+u'\U0001F389', parse_mode='Markdown')