#!/usr/bin/env python3
import argparse
import time
import re

import douyu_api


def report_online(room_list):
    online_str = ' '.join(room_list)
    if len(online_str.strip()) == 0:
        online_str = 'none'
    print('online rooms: {}'.format(online_str))

def get_room_id(astr):
    if re.match(r'\d+', astr):
        return astr
    else:
        return douyu_api.page_parser(astr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--interval', type=int, default=30)
    parser.add_argument('-i', '--input')

    parser.add_argument('url', nargs='?')

    args = parser.parse_args()

    interval = args.interval
    rooms = []
    if args.input:
        with open(args.input, 'r') as fp:
            for line in fp:
                if len(line.strip()) > 0:
                    rooms.append(get_room_id(line.strip()))
    if args.url:
        rooms.append(get_room_id(args.url))

    while True:
        try:
            online_rooms = []
            for room in rooms:
                if douyu_api.douyu_online(room):
                    online_rooms.append(room)
            report_online(online_rooms)
            time.sleep(int(interval))
        except KeyboardInterrupt:
            print('Shutting Down...')
            exit(0)

