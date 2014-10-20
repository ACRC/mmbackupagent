# mmbackup agent

A agent to trigger, monitor and report on the status of mmbackup instances.

`mmbackupagent` is a helper wrapper for IBMs [`mmbackup`](http://www-01.ibm.com/support/knowledgecenter/SSFKCN_3.5.0/com.ibm.cluster.gpfs.v3r5.gpfs100.doc/bl1adm_mmbackup.htm) command. It adds the following features:

 * Triggers concurrent client runs
 * Parses output to send reports to various outputs

## Installation


Installation is done via `setuptools`. Basic installation steps are:

 * `python setup.py build`
 * `python setup.py install`

More options can be found by running `./setup.py --help`

## Configuration


Configuration is kept in YAML form at either `~/.mmbackupagentrc` or `/etc/mmbackupagentrc`. The following configuation options are supported:

### filesystems

This option is required.

A list of filesystems to backup. e.g.

```
filesystems:
 - fs0
 - fs1
```

### mmbackupbin

Default option: `/usr/lpp/mmfs/bin/mmbackup`

The location of the `mmbackup` binary. e.g.

```
mmbackupbin: /usr/lpp/mmfs/bin/mmbackup
```

### resturl

The option is requred if using the `rest` reporting output.

The location of the RESTFUL endpoint for POSTing reports. e.g..

```
resturl: http://localhost:3000
```

### logdir

Defaults option: `/tmp/`

The location for mmbackup to log to. e.g.

```
logdir: /var/log/mmbackup
```

### progressreport

A list of reporting modules to use while reporting on progress. See the reporting section for a description of the different reporting mechimisms.

Progress report plugins are triggered during every state change.

e.g.
```
progressreport:
 - stdout
 - syslog
```

### finalreport

A list of reporting modules to use during the final report. See the reporting section for a description of the different reporting mechimisms.

Final report plugins are triggered at the end of a mmbackup run.

e.g.
```
finalreport:
 - stdout
 - syslog
```
### concurrent

How many filesystem to back up in parrell. e.g.

```
concurrent: 1
```
