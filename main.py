#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import threading

import datastore


def run():
    try:
        parser = argparse.ArgumentParser(description='key value paired datastore')
        parser.add_argument('-k', '--key', type=str, metavar='', required=True, help='Key')
        parser.add_argument('-v', '--value', type=str, metavar='', help='Value')
        parser.add_argument('-c', '--client', type=str, metavar='', required=True, help='Client')
        parser.add_argument('-o', '--operation', type=str, metavar='', required=True, help='Operation')
        parser.add_argument('-p', '--path', type=str, metavar='', help='Path(optional)')
        parser.add_argument('-t', '--time', type=int, metavar='', help='Time to live(optional)')
        args = parser.parse_args()

        # print(args.key, args.value, args.client, args.operation, args.path)
        ds = datastore.DataStore(args.path, args.client)
        if args.operation == 'Create' and args.time:
            ds.Create(args.key, args.value, args.time)
        elif args.operation == 'Create':
            ds.Create(args.key, args.value, 0)
        elif args.operation == 'Read':
            ds.Read(args.key)
        elif args.operation == 'Delete':
            ds.Delete(args.key)
        else:
            print("Choose from operations between 'Create', 'Read' , and 'Delete'")

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    thread = threading.Thread(target=run)
    thread.start()