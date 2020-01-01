#!/usr/bin/python3.6
import tele_util
import time


def getAllLists(chat_id):
    sql = "select name from ls_entry where chat_id=%s group by name"
    rows = tele_util.readSQL(sql, data=[chat_id])
    return [r[0] for r in rows]

def getList(chat_id, name):
    sql = 'select entry from ls_entry where chat_id=%(chat_id)s and name=%(name)s'
    data = {'chat_id': chat_id, 'name': name}
    rows = tele_util.readSQL(sql, data)
    return [r[0] for r in rows]

def addList(chat_id, name, entry):
    sql = '''
        insert into ls_entry (chat_id, name, entry, cts)
        select %(chat_id)s, %(name)s, %(entry)s, %(ts)s from DUAL where not exists (
            select name from ls_entry where chat_id=%(chat_id)s and name=%(name)s and entry=%(entry)s
        ) limit 1
        '''
    data = {'chat_id': chat_id, 'name': name,'entry': entry, 'ts': time.strftime('%Y-%m-%d %H:%M:%S')}
    tele_util.executeSQL(sql, data)

def delList(chat_id, name, entry):
    sql = 'delete from ls_entry where chat_id=%(chat_id)s and name=%(name)s and entry=%(entry)s'
    data = {'chat_id': chat_id, 'name': name,'entry': entry}
    tele_util.executeSQL(sql, data)

def rndList(chat_id, name):
    sql = 'select entry from ls_entry where chat_id=%(chat_id)s and name=%(name)s order by rand()'
    data = {'chat_id': chat_id, 'name': name}
    return tele_util.getOneSQL(sql, data)

def prtList(ls):
    return '["' + '", "'.join(ls) + '"]'