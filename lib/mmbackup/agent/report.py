import json
import datetime
import syslog

def rest(stats):
    j = {"mmbackup":stats}
    data = json.dumps(j)
    headers = {'Content-Type': 'application/json'}

    try:
        request = urllib2.Request("http://localhost:3000/mmbackups.json",data ,headers)
        response = urllib2.urlopen(request)
    except:
        print "WARNING: Could not POST stats"

def stdout(fs,stats):
    print "%s: %s" % (ts(),genstring(fs,stats))

def reportsyslog(fs,stats):
    syslog.openlog('mmbackup')
    syslog.syslog( genstring(fs,stats) )

def genstring(fs,stats):
    stage = stats['stage']
        
    if 'rc' in stats:
        return "%s: status: Finished, started: %s, finished: %s, inspected %s, backedup %s, failed %s, expired %s, transferred %s, rc %s" % (fs,stats['starttime'],stats['endtime'], stats['act_inspected'], stats['act_backedup'],stats['act_failed'],stats['act_expired'],stats['bytes_transferred'],stats['rc'])
    elif stage == 0:
        return "%s: status: Initialising" % (fs)
    elif stage == 1:
        return "%s: status: Scanning filesystem, started: %s" % (fs,stats['starttime'])
    elif stage == 2:
        return "%s: status: Sending Files, started: %s, changed %s, expired %s, unsupported %s" % (fs,stats['starttime'],stats['sched_changed'], stats['sched_expired'], stats['sched_unsupported'])
    elif stage ==3:
        return "%s: status: Finishing, started: %s, finish: %s, inspected %s, backedup %s, failed %s, expired %s, transferred %s" % (fs,stats['starttime'],stats['endtime'], stats['act_inspected'], stats['act_backedup'],stats['act_failed'],stats['act_expired'],stats['bytes_transferred'])

    return ""

def ts():
    return datetime.datetime.now().strftime("%b %d %H:%M:%S")
