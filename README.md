mmbackup agent
==============

A agent to trigger, monitor and report on the status of mmbackup instances.

`mmbackupagent` is a helper wrapper for IBMs [`mmbackup`](http://www-01.ibm.com/support/knowledgecenter/SSFKCN_3.5.0/com.ibm.cluster.gpfs.v3r5.gpfs100.doc/bl1adm_mmbackup.htm) command. It adds the following features:

 * Triggers concurrent client runs
 * Parses output to send reports to various outputs


Configuration
-------------

Configuration is
