import os.path
import sys
import yaml

class Config:
    def __init__(self):
        stream = open(self.findconfigfile(), 'r')
        self.config = yaml.load(stream)

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
