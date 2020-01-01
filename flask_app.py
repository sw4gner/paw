from mysite import tele_util, config, cmds
from flask import Flask, request
import time
import os

os.environ["TZ"] = "Europe/Berlin"
time.tzset()

swagbot = tele_util.startBot(config.swagbot)

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
def telegram_webhook():
    msg = tele_util.MsgUtil(swagbot, request.get_json())
    if msg.cmd in CMD_MAPPING:
        CMD_MAPPING[msg.cmd](msg)
    tele_util.addFile(msg)
    return 'OK'








