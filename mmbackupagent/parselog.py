
import os.path
import re
import dateutil.parser

def parselog(inputfilename):
    stats = {}
    stats['act_inspected'] = 0
    stats['act_backedup'] = 0
    stats['act_updated'] = 0
    stats['act_rebound'] = 0
    stats['act_deleted'] = 0
    stats['act_expired'] = 0
    stats['act_failed'] = 0
    stats['bytes_transferred'] = 0


    # Check file exists
    if not os.path.isfile(inputfilename):
        print "ERROR: Logfile %s not found"%inputfilename
        sys.exit(1)

    stage = 0
    f = open(inputfilename,'r')
    while True:
        line = f.readline()
        if not line: break

        if stage == 0:
            m = re.match(r'mmbackup: Backup of (.*) begins at (.*)\.',line)
            if m:
                stats['filesystem'] = m.group(1)
                stats['starttime'] = dateutil.parser.parse(m.group(2)).isoformat()
                stage += 1
        elif stage == 1:
            m = re.match(r'.*mmbackup:changed.([0-9]+), expired.([0-9]+), unsupported.([0-9]+) for server .(.*)..',line)
            if m:
                stats['sched_changed'] = m.group(1)
                stats['sched_expired'] = m.group(2)
                stats['sched_unsupported'] = m.group(3)
                stats['client'] = m.group(4)
                stage += 1
        elif stage == 2:
            m = re.match(r'mmbackup: TSM Summary Information:',line)
            if m:
                # We have a TSM summary to parse, there could be more than one.
                l = re.match(r'\s*Total number of objects inspected:\s+([0-9]+)',f.readline())
                stats['act_inspected'] += int(l.group(1))
                l = re.match(r'\s*Total number of objects backed up:\s+([0-9]+)',f.readline())
                stats['act_backedup'] += int(l.group(1))
                l = re.match(r'\s*Total number of objects updated:\s+([0-9]+)',f.readline())
                stats['act_updated'] += int(l.group(1))
                l = re.match(r'\s*Total number of objects rebound:\s+([0-9]+)',f.readline())
                stats['act_rebound'] += int(l.group(1))
                l = re.match(r'\s*Total number of objects deleted:\s+([0-9]+)',f.readline())
                stats['act_rebound'] += int(l.group(1))
                l = re.match(r'\s*Total number of objects expired:\s+([0-9]+)',f.readline())
                stats['act_expired'] += int(l.group(1))
                l = re.match(r'\s*Total number of objects failed:\s+([0-9]+)',f.readline())
                stats['act_failed'] += int(l.group(1))
                l = re.match(r'\s*Total number of bytes transferred:\s+([0-9]+)',f.readline())
                stats['bytes_transferred'] += int(l.group(1))
            m = re.match(r'mmbackup: Backup of (.*) completed\s.*\sat\s(.+)\.',line)
            if m:
                stats['endtime'] = dateutil.parser.parse(m.group(2)).isoformat()
                stage += 1
                break
    
    stats['stage'] = stage
    return stats
