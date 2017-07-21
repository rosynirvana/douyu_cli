#! /usr/bin/env python3
import time
import hashlib
import random
import sys
import re
import argparse
import subprocess

import requests

import dyprvt
API_KEY = 'a2053899224e8a92974c729dceed1cc99b3d8282'
VER = '2017063001'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

def dyprvt_hash(input_data):
    return dyprvt.stupidMD5(input_data)

def douyu_online(rid):
    try:
        douyu_api(rid)
    except Exception:
        return False
    return True

def douyu_api_html5(rid):
    endpoint = 'http://m.douyu.com/html5/live?roomId=' + rid
    headers = {}
    headers['User-Agent'] = UA
    req = requests.get(endpoint, headers=headers)
    json_data = req.json()
    if json_data['error'] != 0:
        raise Exception(json_data['msg'])
    return json_data['data']['hls_url']

def douyu_api_android_hd(rid):
    APPKEY = 'Y237pxTx2In5ayGz'
    to_sign = 'room/{0}?aid=androidhd1&cdn={1}&client_sys=android&time={2}'.format(rid, 'ws', int(time.time()))
    sign = hashlib.md5(bytes(to_sign+APPKEY, 'utf8')).hexdigest()
    endpoint = 'https://capi.douyucdn.cn/api/v1/{0}&auth={1}'.format(to_sign, sign)
    json_data = requests.get(endpoint).json()
    if json_data['error'] != 0:
        raise Exception(json_data['data'])
    return json_data['data']['rtmp_url'] + '/' + json_data['data']['rtmp_live']

def douyu_api(rid, cdn='ws', rate='1'):
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
        return url
    elif json_data['error'] == -5:
        raise Exception('Offline')
    else:
        raise Exception('API returned with error {}'.format(json_data['error']))

def page_parser(url):
    page_content = requests.get(url).content.decode('utf8')
    online_patt = r'"online_id":\[([0-9,"]+)\]'
    hit = re.search(online_patt, page_content)
    if hit is not None:
        print('An event page with room ids:')
        print(hit.group(1))
        room_list = hit.group(1).split(',')
        room = room_list[0] if len(room_list) > 1 else room_list
        return room[1:-1]
    else:
        hit = re.search(r'"room_id":(\d+)', page_content)
        if hit is not None:
            return hit.group(1)

    return None

if __name__ == '__main__':
    print('status: seems broken')
    print('You can check {} for info of progress'.format('https://github.com/spacemeowx2/DouyuHTML5Player/issues/28'))
    #sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--room')
    parser.add_argument('-q', '--quality', choices=['0', '1', '2'])

    grp = parser.add_mutually_exclusive_group()
    grp.add_argument('-p', '--mpv', action='store_true')
    grp.add_argument('-s', '--record')

    parser.add_argument('url', nargs='?')
    args = parser.parse_args()

    if args.room:
        rid = args.room
    elif args.url:
        rid = page_parser(args.url)

    quality = args.quality if args.quality else '0'
    try:
        #video_url = douyu_api(rid, rate=quality)
        #video_url = douyu_api_html5(rid)
        video_url = douyu_api_android_hd(rid)
    except Exception as e:
        print(e)
        sys.exit(0)

    if args.mpv:
        subprocess.call(['mpv', '--no-ytdl', video_url])
    elif args.record:
        out_fn = args.record + '.mp4'
        subprocess.call(['ffmpeg', '-i', video_url, '-c', 'copy', out_fn])
    else:
        print(video_url)

