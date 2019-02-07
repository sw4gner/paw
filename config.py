import telepot
import MySQLdb
import urllib3



telegram = {
    'api_key': '716856099:AAFimr918ZMBaN3LG91WqSWe2cKYTqs7SRg',
    'proxy_url': 'http://proxy.server:3128',
    'hook_dom': 'https://swa9ner.pythonanywhere.com',
    'hook_path': '/Telegram/2352',
    'num_pools': 1,
    'maxsize': 10,
    'retries': False,
    'timeout': 30,
}

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(telegram['api_key'])

def getCon():
    return MySQLdb.connect(
        host='fia4awagner.mysql.pythonanywhere-services.com',
        user='fia4awagner',
        passwd='fia4awagnerfia4awagner',
        database='fia4awagner$default')