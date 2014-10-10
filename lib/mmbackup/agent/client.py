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
            self.finalreport()
        elif self.stats != newstats:
            self.stats = newstats
            self.progressreport()

        return rc

    def finalreport(self):
        report.stdout(self.filesystem,self.stats)
        report.reportsyslog(self.filesystem,self.stats)
        #report.poststats(self.stats)

    def progressreport(self):
        report.stdout(self.filesystem,self.stats)
        report.reportsyslog(self.filesystem,self.stats)
        #report.poststats(self.stats)
