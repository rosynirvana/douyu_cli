#! /usr/bin/env python3
import time
import hashlib
import random
import json
import sys
import re

import requests

import dyprvt
API_KEY = 'a2053899224e8a92974c729dceed1cc99b3d8282'
VER = '2017061511'

def dyprvt_hash(input_data):
    return dyprvt.stupidMD5(input_data)

def douyu_api(rid, cdn='ws', rate='2', did=None, tt=None):
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
    elif json_data['error'] == -5:
        raise Exception('Offline')
    else:
        raise Exception('API returned with error {}'.format(json_data['error']))


if __name__ == '__main__':
    rid = re.search(r'(\d+)', sys.argv[1])
    if rid is not None:
        rid = rid.group(1)
        douyu_api(rid)
