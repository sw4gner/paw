#!/usr/bin/python3.6
from contextlib import closing
import config
import json
import random

def savNew(chat_id, name, entry):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute("select list from list where chat_id='%s' and name='%s'" % (chat_id, name))
            r = cur.fetchone()
            if r != None:
                insrt = False
                lst = json.loads(r[0])
            else:
                insrt = True
                lst = []
        lenBfr = len(lst)
        lst.append(entry)
        if len(set(lst)) != lenBfr:
            with closing(con.cursor()) as cur:
                if insrt:
                    sql = "insert into list values (%s, '%s', '%s')" % (chat_id, name, json.dumps(lst))
                else:
                    sql = "update list set list='%s' where chat_id='%s' and name='%s'" %  (json.dumps(lst), chat_id, name)
                cur.execute(sql)
                con.commit()
        else:
            lst = list(set(lst))
    return json.dumps(lst)

def getList(chat_id, name):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute("select list from list where chat_id='%s' and name='%s'" % (chat_id, name))
            r = cur.fetchone()
            if r == None:
                return '[]'
            return r[0]

def getRandomFromList(chat_id, name):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute("select list from list where chat_id='%s' and name='%s'" % (chat_id, name))
            r = cur.fetchone()
            if r == None:
                return None
            a = json.loads(r[0])
            random.shuffle(a)
            return a[0]

def removeFromList(chat_id, name, val):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute("select list from list where chat_id='%s' and name='%s'" % (chat_id, name))
            r = cur.fetchone()
            if r == None:
                return None
            a = json.loads(r[0])
            if val in a:
                a.remove(val)
                sql = "update list set list='%s' where chat_id='%s' and name='%s'" %  (json.dumps(a), chat_id, name)
                cur.execute(sql)
                con.commit()
            return json.dumps(a)

def getRandomList(chat_id, name):
    with closing(config.getCon()) as con:
        with closing(con.cursor()) as cur:
            cur.execute("select list from list where chat_id='%s' and name='%s'" % (chat_id, name))
            r = cur.fetchone()
            if r == None:
                return '[]'
            a = json.loads(r[0])
            random.shuffle(a)
            return json.dumps(a)