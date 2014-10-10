import os.path
import sys
import yaml

class Config:
    def __init__(self):
        stream = open(self.findconfigfile(), 'r')
        self.config = yaml.load(stream)

        if 'progressreport' not in self.config:
            self.config['progressreport'] = ['stdout']
        if 'finalreport' not in self.config:
            self.config['finalreport'] = ['stdout']
        if 'resturl' not in self.config:
            if 'rest' in self.config['progressreport'] or \
               'rest' in self.config['finalreprt']:
                   print "ERROR: rest reporting in progressreport or finalreport config but no resturl set"
                   sys.exit(1)
        if 'filesystems' not in self.config:
            print "ERROR: You must specify at least one filesystem to backup in the config"
            sys.exit(1)
        if 'mmbackupbin' not in self.config:
            self.config['mmbackupbin'] = "/usr/lpp/mmfs/bin/mmbackup"
        if 'logdir' not in self.config:
            self.config['logdir'] = "/tmp/"

    def findconfigfile(self):
        """
        Find a valid config file to load on the filesystem
        """

        # A ordered list of possible config files
        configfiles = ["~/.mmbackupagentrc",
                       "/etc/mmbackupagentrc"]

        for configfile in configfiles:
            if os.path.isfile(os.path.expanduser(configfile)):
                return os.path.expanduser(configfile)

        # No valid config file found
        print "ERROR: No valid config file found in any of the following locations:" 
        for configfile in configfiles:
            print " - %s" % configfile
        sys.exit(1)
