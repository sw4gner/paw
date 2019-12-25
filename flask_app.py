'''
Created on Dec 1, 2019

@author: swa
'''

import tele_util, config, cmds
from flask import Flask, request, send_file
import time


swagbot = tele_util.startBot(config.swagbot)

app = Flask(__name__)


@app.route(config.swagbot['hook'], methods=['POST'])
def telegram_webhook():
    upd=request.get_json()
    msg = tele_util.MsgUtil(swagbot, request.get_json())
    if msg.cmd in CMD_MAPPING:
        CMD_MAPPING[msg.cmd](msg)
        return 'OK'
    if 'message' in upd:
        if 'photo' in upd['message']:
            addPhoto(upd['message']['photo'][0]['file_id'], 'p')
        if 'animation' in upd['message']:
            addPhoto(upd['message']['animation']['file_id'], 'g')
        return "OK"
    return 'OK'




CMD_MAPPING = {
    'zitat': cmds.zitat,
    'gif': cmds.gif,
    'tenor': cmds.tenor,
    'list': cmds.list,
    'roulette': cmds.roulette,
    'bit': cmds.bit,
    'svb': cmds.sendViaBot,
}

def addPhoto (file_id, typ3):
    sql = '''
    INSERT INTO daylie_post (file_id, type, date_day,tags, cts)
    SELECT '%(f)s', '%(t)s', '', 'b', '%(ts)s' FROM DUAL WHERE NOT EXISTS (
        SELECT file_id FROM daylie_post WHERE file_id = '%(f)s'
    ) LIMIT 1'''
    data = {'f':file_id, 't': typ3, 'ts': time.strftime('%Y-%m-%d %H:%M:%S')}
    tele_util.executeSQL(sql, data)


