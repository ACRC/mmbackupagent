#!/usr/bin/env python

import argparse
import sys
import pprint
import urllib2
import urllib
import config
import time

import client


class Agent:
    def __init__(self):
        self.config = config.Config()
        self.clients = {}

        self.filesystems = self.config.config['filesystems'] 

            
        self.mainloop()

    def mainloop(self):
        while True:
            self.addclients()
            finishedprocs = []
            for key in self.clients:
                if self.clients[key].checkprogress() != None:
                    finishedprocs.append(key)

            for key in finishedprocs:
                p = self.clients.pop(key,None)
                if p:
                    del p

            if len(self.clients) == 0 and len(self.filesystems) == 0:
                return 0
            time.sleep(10)

    def addclients(self):
        while True:
            if len(self.filesystems) == 0:
                break
            if len(self.clients) < self.config.config['concurrent']:
                filesystem = self.filesystems.pop()
                self.clients[filesystem] = client.Client(filesystem,self.config)
            else:
                break

