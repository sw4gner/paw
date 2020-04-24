import tele_util, config, cmds, crab, stats
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
    'quiz': cmds.quiz,
    'trivia': cmds.trivia,
    'truth': cmds.truth,
    'dare2': cmds.dare,
    'stats': cmds.stats,
}

@app.route(config.swagbot['hook'], methods=['POST'])
@tele_util.tryAndLogError
def swagbot_hook():
    msg = tele_util.MsgUtil(swagbot, request.get_json())
    if msg and not msg.hasmsg:
        return 'OK'
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

triviabot = tele_util.startBot(config.triviabot)
@app.route(config.triviabot['hook'], methods=['POST'])
@tele_util.tryAndLogError
def triviabot_hook():
    msg = tele_util.MsgUtil(triviabot, request.get_json())
    if msg.cmd == 'trivia':
        cmds.trivia(msg, config=config.triviabot)
    return "OK"


crabbot = tele_util.startBot(config.crabtelegram)

@app.route(config.crabtelegram['hook'], methods=['POST'])
@tele_util.tryAndLogError
def crabbot_hook():
    msg = tele_util.MsgUtil(crabbot, request.get_json())
    if msg.cmd == 'silence':
        crab.createOutPng(msg.txt)
        msg.send('', typ='p', file='/home/fia4awagner/mysite/img/out.png')
    return "OK"

@app.route('/groupstats/<groupid>')
def groupstats(groupid):
    data = stats.getData(groupid, request)
    users = stats.getUser(data)

    out = {
        'groupid': data['chat_id'],
        'groupname': 'idb with friends',
        'scalestart': data['start'],
        'scaleend': data['end'],
        'btnday': True,
        'linelabels': ['%02d:00' % i for i in range(0,24)],
        'linedata': stats.getLinedata(data, users),
        'users': users,
        'chart1': stats.getChart1(data),
        'chart2': stats.getChart2(data),
        'chart3': stats.getChart3(data),
    }
    return render_template('group_stats.html', **out)

@app.route('/sensordata/put', methods=['POST'])
@tele_util.tryAndLogError
def put_sensor_data():
    json = request.get_json()
    data = {'sensor': json['sensor'],
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'temp': int(json['temp']),
            'humidity': int(json['humidity']),}
    sql = 'insert into sensor_data value (%(sensor)s, %(time)s, %(temp)s, %(humidity)s);'
    tele_util.executeSQL(sql, data)
    return "OK"




