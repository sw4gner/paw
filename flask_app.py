import tele_util, config, cmds, crab
from flask import Flask, request, render_template
import time
import os

os.environ["TZ"] = "Europe/Berlin"
time.tzset()
app = Flask(__name__)


swagbot = tele_util.startBot(config.swagbot)
CMD_MAPPING = {
    'zitat': cmds.zitat,
    'gif': cmds.gif,
    'tenor': cmds.tenor,
    'list': cmds.list_,
    'roulette': cmds.roulette,
    'bit': cmds.bit,
    'svb': cmds.sendViaBot,
    'daily': cmds.dailyPost,
    'roll': cmds.rollFunc,
    'prop': cmds.props,
}

@app.route(config.swagbot['hook'], methods=['POST'])
@tele_util.tryAndLogError
def swagbot_hook():
    msg = tele_util.MsgUtil(swagbot, request.get_json())
    if msg.cmd in CMD_MAPPING:
        CMD_MAPPING[msg.cmd](msg)
    if 'Y' == tele_util.getProp(msg.getChatId(), 'addFile', default='N'):
        tele_util.addFile(msg)
    if 'Y' != tele_util.getProp(msg.getChatId(), 'MsgLog/deaktivate', default='N'):
        tele_util.updateMsgLog(msg.upd)
    return 'OK'


dnbot = tele_util.startBot(config.dntelegram)

@app.route(config.dntelegram['hook'], methods=['POST'])
@tele_util.tryAndLogError
def dnbot_hook():
    m = request.get_json()
    if m.get('message', {}).get('photo', None):
        sql = """
        insert into photo values
        select '%(f)s' from DUAL where not exists (
            select file_id from photo where file_id = '%(f)s'
        ) limit 1""" % {'f': m['message']['photo'][0]['file_id']}
        tele_util.executeSQL(sql)
    return "OK"


crabbot = dnbot = tele_util.startBot(config.crabtelegram)

@app.route(config.crabtelegram['hook'], methods=['POST'])
@tele_util.tryAndLogError
def crabbot_hook():
    msg = tele_util.MsgUtil(crabbot, request.get_json())
    if msg.cmd == 'silence':
        crab.createOutPng(msg.txt)
        msg.send('', typ='p', file='/home/fia4awagner/mysite/img/out.png')
    return "OK"


@app.route('/groupstats/<groupid>')
def groupstats(groupid, **kwargs):
    data = {
        'groupid': -1999999,
        'groupname': 'idb with friends',
        'scalestart': '2019-8-01',
        'scaleend': '2019-8-01',
        'btnmonth': True,
        'linelabels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        'users': [
            {
                'name': 'SWAGNER',
                'rank':1,
                'linedata': [300,500,44,321,123,452,5],
                'posts': 1237,
                'type': {'gif': 4, 'messages': 9,'commands': 3,},
                'textlen':40000,
            }, {
                'name': 'SWAGNER#2',
                'rank':2,
                'linedata': [1300,520,443,31,1123,952,80],
                'posts': 3237,
                'type': {'gif': 20, 'messages': 2,'commands': 0,},
                'textlen':78000,
            },
        ],
        'chart1': [['SWAGNER', 30],['SWAGNER#2', 70],],
        'chart2': [['gif', 2],['commands', 6],['messages', 9],],
        'chart3': [['SWAGNER', 40000],['SWAGNER#2', 78000],],
    }
    return render_template('group_stats.html', **data)
