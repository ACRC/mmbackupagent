import json
import datetime

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
    stage = stats['stage']
        
    if 'rc' in stats:
        print "%s %s: start: %s, status: Finished, finish: %s, inspected %s, backedup %s, failed %s, expired %s, transferred %s, rc %s" % (ts(),fs,stats['starttime'],stats['endtime'], stats['act_inspected'], stats['act_backedup'],stats['act_failed'],stats['act_expired'],stats['bytes_transferred'],stats['rc'])
    if stage == 0:
        print "%s %s: status: Initialising" % (ts(),fs)
    elif stage == 1:
        print "%s %s: started: %s, status: Scanning filesystem" % (ts(),fs,stats['starttime'])
    elif stage == 2:
        print "%s %s: start: %s, status: Sending Files, changed %s, expired %s, unsupported %s" % (ts(),fs,stats['starttime'],stats['sched_changed'], stats['sched_expired'], stats['sched_unsupported'])
    elif stage ==3:
        print "%s %s: start: %s, status: Finishing, finish: %s, inspected %s, backedup %s, failed %s, expired %s, transferred %s" % (ts(),fs,stats['starttime'],stats['endtime'], stats['act_inspected'], stats['act_backedup'],stats['act_failed'],stats['act_expired'],stats['bytes_transferred'])
    else:
        print "%s:" % fs
        for key in stats:
            print " - %s: %s" % (key,stats[key])

def ts():
    return datetime.datetime.now().strftime("%b %d %H:%M:%S")
