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

        filesystems = self.config.config['filesystems'] 

        for filesystem in filesystems:
            self.clients[filesystem] = client.Client(filesystem,self.config)
            
        self.checkprogress()

    def checkprogress(self):
        while True:
            finishedprocs = []
            for key in self.clients:
                if self.clients[key].checkprogress() != None:
                    finishedprocs.append(key)

            for key in finishedprocs:
                p = self.clients.pop(key,None)
                if p:
                    del p

            if len(self.clients) == 0:
                return 0
            time.sleep(10)

