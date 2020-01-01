from mysite import tele_util, config, cmds
from flask import Flask, request
import time
import os

os.environ["TZ"] = "Europe/Berlin"
time.tzset()

swagbot = tele_util.startBot(config.swagbot)
dnbot = tele_util.startBot(config.dntelegram)

app = Flask(__name__)

CMD_MAPPING = {
    'zitat': cmds.zitat,
    'gif': cmds.gif,
    'tenor': cmds.tenor,
    'list': cmds.list,
    'roulette': cmds.roulette,
    'bit': cmds.bit,
    'svb': cmds.sendViaBot,
    'daily': cmds.dailyPost,
}

@app.route(config.swagbot['hook'], methods=['POST'])
@tele_util.tryAndLogError
def swagbot():
    msg = tele_util.MsgUtil(swagbot, request.get_json())
    if msg.cmd in CMD_MAPPING:
        CMD_MAPPING[msg.cmd](msg)
    tele_util.addFile(msg)
    return 'OK'


@app.route(config.dntelegram['hook'], methods=['POST'])
@tele_util.tryAndLogError
def dnidb():
    m = request.get_json()
    if m.get('message', {}).get('photo', None):
        sql = """
        insert into photo values
        select '%(f)s' from DUAL where not exists (
            select file_id from photo where file_id = '%(f)s'
        ) limit 1""" % {'f': m['message']['photo'][0]['file_id']}
        tele_util.executeSQL(sql)
    return "OK"





