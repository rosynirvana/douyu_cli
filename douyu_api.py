#! /usr/bin/env python3
import time
import hashlib
import random
import sys
import re

import requests

import dyprvt
API_KEY = 'a2053899224e8a92974c729dceed1cc99b3d8282'
VER = '2017063001'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

def dyprvt_hash(input_data):
    return dyprvt.stupidMD5(input_data)

def douyu_api(rid, cdn='ws', rate='0'):
    endpoint = 'https://www.douyu.com/lapi/live/getPlay/' + rid
    tt = str(int(time.time() / 60))
    rnd_md5 = hashlib.md5(str(random.random()).encode('utf8'))
    did = rnd_md5.hexdigest().upper()
    to_sign = ''.join([rid, did, API_KEY, tt])
    sign = dyprvt_hash(to_sign)
    payload = dict(ver=VER, sign=sign, did=did, rate=rate, tt=tt, cdn=cdn)
    headers = {}
    headers['User-Agent'] = UA

    json_data = requests.post(endpoint, data=payload, headers=headers).json()

    if json_data['error'] == 0:
        data = json_data['data']
        url = '/'.join([data['rtmp_url'], data['rtmp_live']])
        print(url)
    elif json_data['error'] == -5:
        raise Exception('Offline')
    else:
        raise Exception('API returned with error {}'.format(json_data['error']))


if __name__ == '__main__':
    #rid = re.search(r'/(\d+)', sys.argv[1])
# what if room name is 123abc ?
    page_content = requests.get(sys.argv[1]).content.decode('utf8')
    rid = re.search(r'room_id=(\d+)', page_content)
    if rid is not None:
        rid = rid.group(1)
        try:
            douyu_api(rid)
        except Exception as e:
            print(e)

