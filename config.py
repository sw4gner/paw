import telepot
import MySQLdb
import urllib3

sysuser = 547975832
site = 'https://fia4awagner.pythonanywhere.com'
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

def startBot(conf):
    bot = telepot.Bot(conf['api_key'])
    bot.setWebhook(site+conf['hook'], max_connections=1)
    return bot

def getCon():
    return MySQLdb.connect(
        host='',
        user='',
        passwd='',
        database='')

swagbot = {
    'api_key': '',
    'hook': '',
}
bot = startBot(swagbot)

dntelegram = {
    'api_key': '',
    'hook': '',
}
botdnbot = None # startDnidB(dntelegram):


def notifySysUser(msg):
    bot.sendMessage(sysuser, msg, parse_mode='Markdown')