import parselog
import os.path
import subprocess

import report

class Client:
    def __init__(self,filesystem,config):
        self.config = config 
        self.filesystem = filesystem
        self.stats = {}
        
        mmbackupbin = os.path.expanduser(self.config.config['mmbackupbin'])
        if not os.path.isfile(mmbackupbin):
            print "ERROR: cannot find mmbackup binary at %s."%mmbackupbin
            sys.exit(1)

        logdir = os.path.expanduser(self.config.config['logdir'])

        self.logfilename=logdir+"/bar-"+filesystem
        self.log = open(self.logfilename,'w')
        self.proc = subprocess.Popen([mmbackupbin,filesystem],stdout=self.log)

    def __del__(self):
        self.log.close()

    def checkprogress(self):
        newstats = parselog.parselog(self.logfilename)
        rc = self.proc.poll()
        if rc != None:
            newstats['rc'] = rc
            self.stats = newstats
            self.report('finalreport')
        elif self.stats != newstats:
            self.stats = newstats
            self.report('progressreport')

        return rc

    def report(self,type):
        if 'stdout' in self.config.config[type]:
            report.stdout(self.filesystem,self.stats)
        if 'syslog' in self.config.config[type]:
            report.reportsyslog(self.filesystem,self.stats)
        if 'rest' in self.config.config[type]:
            report.rest(self.stats)
