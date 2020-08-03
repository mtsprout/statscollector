#!/usr/bin/env python

import os
import commands
import urllib
import urllib2

influxLines = []
influxHost = "localhost"
influxDB = "perf"
influxURL = "http://" + influxHost+ ":8086/write?db=perf"

hostName = os.uname()[1]

cpuInfo = commands.getoutput("sar 1 1 | tail -1").split()
cpuLine = "cpu,host=" + hostName + \
    " user=" + cpuInfo[2] \
    + ",system=" + cpuInfo[4] \
    + ",idle=" + cpuInfo[7] \
    + ",iowait=" + cpuInfo[5] \
    + ",nice=" + cpuInfo[3]
influxLines.append(cpuLine)

partitionList = commands.getoutput("df | egrep -v 'tmp|run|cgroup|Filesystem' | tr '%' ' '").split("\n")
for partition in partitionList:
  partInfo = partition.split()
  diskTotal = int(partInfo[1]) * 1024
  diskUsed = int(partInfo[2]) * 1024
  diskAvail = int(partInfo[3]) * 1024
  partitionLine = "partition,host=" + hostName \
     + ",mountpoint=" + partInfo[5] \
     + " totalsize=" + str(diskTotal) \
     + ",diskused=" + str(diskUsed) \
     + ",diskavail=" + str(diskAvail) \
     + ",percentused=" + str(partInfo[4]) 
  influxLines.append(partitionLine)

loadInfo = commands.getoutput("cat /proc/loadavg").split()
cpuCount = commands.getoutput("grep -c processor /proc/cpuinfo")
loadLine = "load,host=" + hostName + \
    " fifteenMinute=" + loadInfo[0] \
    + ",fiveMinute=" + loadInfo[1] \
    + ",oneMinute=" + loadInfo[2] \
    + ",cpus=" + cpuCount
influxLines.append(loadLine)

blockInfo = commands.getoutput("vmstat | tail -1").split()
rwInfo = commands.getoutput("sar -b | tail -1").split()
ioLine = "iops,host=" + hostName + \
    " bi=" + blockInfo[8] \
    + ",bo=" + blockInfo[9] \
    + ",rps=" + rwInfo[4] \
    + ",wps=" + rwInfo[5]
influxLines.append(loadLine)

for line in influxLines:
  request = urllib2.Request(influxURL, data=line)
  response = urllib2.urlopen(request)
