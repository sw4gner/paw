#!/usr/bin/python3.6
from quotes import daylieQuote
from datetime import date
import config


daylieQuote()

if str(date.today()) == '2019-11-21' or str(date.today()) == '2019-09-18':
    config.notifySysUser('Webapp/Task will be disabled')