import tele_util
import datetime


def getData(group_id, req):
    t = datetime.date.today().replace(day=1)
    end = t - datetime.timedelta(days=1)
    start = end.replace(day=1)
    data = {'chat_id': str(group_id), 'start': start.strftime('%Y-%m-%d'),'end': end.strftime('%Y-%m-%d'),}
    if req.args.get('scaleend'):
        data['end']=req.args.get('scaleend')
    if req.args.get('scalestart'):
        data['start']=req.args.get('scalestart')
    return data

def getUser(data):
    sql = '''
    select nme, count(*) as posts, sum(len)
        , sum(case type when 't' then 1 else 0 end) as t
        , sum(case type when 'a' then 1 else 0 end) as a
        , sum(case type when 's' then 1 else 0 end) as s
        , sum(case type when 'p' then 1 else 0 end) as p
        , sum(case type when 'v' then 1 else 0 end) as v
        , sum(case type when 'i' then 1 else 0 end) as i
        , sum(case type when 'p' then 1 else 0 end) as o
        , sum(case type when 'd' then 1 else 0 end) as d
        , sum(case type when 'c' then 1 else 0 end) as c
        , sum(case type when 'N' then 1 else 0 end) as n
    from msglog l
    left join user_name u on u.user_id=l.user_id
    where l.chat_id=%(chat_id)s and l.date between %(start)s and %(end)s
    group by nme, u.user_id order by posts desc;'''
    users = []
    for r in tele_util.readSQL(sql, data=data):
        tele_util.typ3s
        types = {}
        for idx,(_,name) in enumerate(tele_util.typ3s.items()):
            if r[idx+3]!=0:
                types[name] = int(r[idx+3])
        user = {'name': r[0], 'posts': r[1],'textlen': r[2],'type': types,}
        users.append(user)
    return users

def getChart1(data):
    sql = '''
    select nme,
    count(*)/(select count(*) from msglog where l.chat_id=%(chat_id)s and l.date between %(start)s and %(end)s) * 100
    from msglog l left join user_name u on u.user_id=l.user_id
    where l.chat_id=%(chat_id)s and l.date between %(start)s and %(end)s
    group by chat_id,nme;'''
    chart1=[]
    for r in tele_util.readSQL(sql, data=data):
        chart1.append([r[0], r[1]])
    return chart1

def getChart2(data):
    sql = '''
    select sum(case type when 't' then 1 else 0 end) as t
        , sum(case type when 'a' then 1 else 0 end) as a
        , sum(case type when 's' then 1 else 0 end) as s
        , sum(case type when 'p' then 1 else 0 end) as p
        , sum(case type when 'v' then 1 else 0 end) as v
        , sum(case type when 'i' then 1 else 0 end) as i
        , sum(case type when 'p' then 1 else 0 end) as o
        , sum(case type when 'd' then 1 else 0 end) as d
        , sum(case type when 'c' then 1 else 0 end) as c
        , sum(case type when 'N' then 1 else 0 end) as n
    from msglog
    where chat_id=%(chat_id)s and date between %(start)s and %(end)s
    group by chat_id;'''
    chart2=[]
    rows = tele_util.readSQL(sql, data=data)
    if len(rows) == 0:
        return []
    r = rows[0]
    for idx,(_,name) in enumerate(tele_util.typ3s.items()):
        if r[idx] > 0:
            chart2.append([name, r[idx]])
    return chart2
def getChart3(data):
    sql = '''
    select nme, sum(len)
    from msglog l left join user_name u on u.user_id=l.user_id
    where l.chat_id=%(chat_id)s and l.date between %(start)s and %(end)s
    group by chat_id,nme;'''
    chart3=[]
    for r in tele_util.readSQL(sql, data=data):
        chart3.append([r[0], r[1]])
    return chart3

def getLinedata(data, users):
    userlinedata={}
    for u in users:
        d={}
        for i in range(0,24):
            d['%02d' % i]=0
        userlinedata[u['name']]=d
    sql = '''
    select u.nme, SUBSTRING(time from 1 for 2) as h, count(*) as c
    from msglog l left join user_name u on u.user_id=l.user_id
    where l.chat_id=%(chat_id)s and l.date between %(start)s and %(end)s
    group by l.chat_id, l.user_id, SUBSTRING(time from 1 for 2) order by l.user_id;
    '''
    for row in tele_util.readSQL(sql, data=data):
        nme, h, cnt = row
        userlinedata.get(nme, {})[h] = cnt

    linedata = []
    for _,t in userlinedata.items():
        line = []
        for _, val in t.items():
            line.append(val)
        linedata.append(line)
    return linedata
