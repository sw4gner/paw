import requests
import json
import random



apikey='NdNjS0WAi0UgWtjl2fYRnrKo6pWJB8Vi'


def getRand (term):
    r = requests.get("http://api.giphy.com/v1/gifs/search?lang=de&api_key=%s&q=%s&rating=R&limit=1&offset=%s" % (apikey, term, random.randint(1,10)))
    if r.status_code == 200:
        jobj = json.loads(r.content)
        if 'data' in jobj and len(jobj['data'])>0:
            return jobj['data'][0]['images']["original"]["url"].replace('\/', '/')
        else:
            return None
    else:
        return None


tenor_apiKey = 'I5PUSNT8CNTY'

def getRandTenor(term):
    r = requests.get("https://api.tenor.com/v1/random?key=%s&limit=1&q=%s&locale=de_GER" % (tenor_apiKey, term))
    if r.status_code == 200:
        jobj = json.loads(r.content)
        if 'results' in jobj and len(jobj['results'])>0:
            return jobj['results'][0]["url"]
        else:
            return None
    else:
        return None

nxt=''
def getTrendTenor():
    global nxt
    r = requests.get("https://api.tenor.com/v1/trending?key=%s&locale=de_GER&limit=1&pos=%s" % (tenor_apiKey, nxt))
    if r.status_code == 200:
        jobj = json.loads(r.content)
        if 'results' in jobj and len(jobj['results'])>0:
            nxt=jobj['next']
            return jobj['results'][0]["url"]
        else:
            return None
    else:
        return None