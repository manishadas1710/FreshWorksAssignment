# -*- coding: utf-8 -*-

import json
import os.path
import sys
from datetime import datetime, timedelta


class DataStore:
    json_object = None
    path = ''
    client = ''

    def __init__(self, path, client):
        if os.path.isfile('client.log'):
            f = open("client.log", "r+")
            if f.read() == "1":
                print("Someone else is using. Try after sometime")  # preventing multiple clients from accessing the file
                return
            f.close()
        f = open("client.log", "w+")
        f.write("1")
        f.close()
        self.path = path
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as openfile:
                    self.json_object = json.load(openfile)

        except:
            #self.path = client + ".json"
            self.path = r"C:\Users\MANISHA\Desktop\Freshworks_Assignment" + client + ".json"
            if os.path.exists(self.path):
                with open(self.path, 'r') as openfile:
                    self.json_object = json.load(openfile)
        # print(self.path)

    def Create(self, key, val, time):
        exp = datetime.now() + timedelta(seconds=time)
        exp_string = exp.strftime("%H:%M:%S")
        #print(exp_string)
        if len(key) > 32:
            print('Length of key exceeded')
            return
        if sys.getsizeof(val) > 16 * 1024:
            print('Size of value too high(> 16KB)')
            return
        if not val:
            print('Enter value!')
            return

        if time == 0:
            if os.path.exists(self.path) and key not in self.json_object.keys():
                self.json_object[key] = {
                    "value": val,
                }
            elif not os.path.exists(self.path):
                self.json_object = {
                    key: {
                        "value": val,
                    }
                }
            else:
                print("Key already exists")
                return
            # print(self.json_object)
            with open(self.path, "w+") as outfile:
                json.dump(self.json_object, outfile)
                print("Added new entry")
            return

        if os.path.exists(self.path) and key not in self.json_object.keys():
            self.json_object[key] = {
                "value": val,
                "expiry": exp_string
            }
        elif not os.path.exists(self.path):
            self.json_object = {
                key: {
                    "value": val,
                    "expiry": exp_string
                }
            }
        else:
            print("Key already exists")
            return
        # print(self.json_object)
        with open(self.path, "w+") as outfile:
            json.dump(self.json_object, outfile)
            print("Added new entry")

    def Read(self, key):
        if os.path.exists(self.path) and key in self.json_object.keys():
            print(self.json_object[key]['value'])
        else:
            print("Key doesn't exist")

    def Delete(self, key):
        if os.path.exists(self.path) and key in self.json_object.keys():
            self.json_object.pop(key)

            with open(self.path, "w+") as outfile:
                json.dump(self.json_object, outfile)
                print("Deleted an entry")
        else:
            print("Key doesn't exist")

        # print(self.json_object)

    def __del__(self):
        f = open("client.log", "w+")  # letting other clients to access the file when the process ends
        f.write("0")
        f.close()