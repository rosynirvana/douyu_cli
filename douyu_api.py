import time
import hashlib
import random
import json

import requests

import dyprvt
API_KEY = 'a2053899224e8a92974c729dceed1cc99b3d8282'
VER = '2017061511'

def dyprvt_hash(input_data):
    return dyprvt.stupidMD5(input_data)

def douyu_api(rid, cdn, rate, did=None, tt=None):
    endpoint = 'https://www.douyu.com/lapi/live/getPlay/' + rid
    if tt is None:
        tt = str(int(time.time() / 60))
    if did is None:
        rnd_md5 = hashlib.md5(str(random.random()).encode('utf8'))
        did = rnd_md5.hexdigest().upper()
    to_sign = ''.join([rid, did, API_KEY, tt])
    sign = dyprvt_hash(to_sign)
    payload = dict(ver=VER, sign=sign, did=did, rate=rate, tt=tt, cdn=cdn)
    payload_str = 'ver={}&sign={}&did={}&rate={}&tt={}&cdn={}'.format(VER, sign, did, rate, tt, cdn)

    json_str = requests.post(endpoint, data=payload).content.decode('utf8')
    json_data = json.loads(json_str)

    if json_data['error'] == 0:
        data = json_data['data']
        url = '/'.join([data['rtmp_url'], data['rtmp_live']])
        print(url)
    else:
        raise Exception('API returned with error')


#douyu_api('532152', '1', '', '72D26C8FF690BE48BCD16357AFB3758F', '24962932')
douyu_api('242967', 'ws', '2')
#douyu_api('2150067', 'ws', '2', '72D26C8FF690BE48BCD16357AFB3758F', '24964521')
#douyu_api('2150067', 'ws', '2')

