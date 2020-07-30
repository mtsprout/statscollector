#!/bin/bash

INFLUXHOST=localhost
INFLUXDB=perf

# HOSTNAME
HOSTNAME=$(hostname -s)

# CPU INFO
USER=$(sar 1 1 | tail -1 | awk '{print $3}')
NICE=$(sar 1 1 | tail -1 | awk '{print $4}')
SYSTEM=$(sar 1 1 | tail -1 | awk '{print $5}')
IOWAIT=$(sar 1 1 | tail -1 | awk '{print $6}')
IDLE=$(sar 1 1 | tail -1 | awk '{print $8}')

# SWAP INFO
TOTALSWAP=$(cat /proc/meminfo | grep SwapTotal | awk '{print $2'})
FREESWAP=$(cat /proc/meminfo | grep SwapFree | awk '{print $2'})
USEDSWAP=$(( ${TOTALSWAP} - ${FREESWAP} ))

# MEMORY INFO
TOTALMEM=$(cat /proc/meminfo | grep MemTotal | awk '{print $2'})
FREEMEM=$(cat /proc/meminfo | grep MemFree | awk '{print $2'})
CACHEUSAGE=$(cat /proc/meminfo | grep ^Cached | awk '{print $2'})
AVAILABLE=$(cat /proc/meminfo | grep Available | awk '{print $2'})

# LOAD INFO
FIFTEENMINUTE=$(cat /proc/loadavg | awk '{print $1}')
FIVEMINUTE=$(cat /proc/loadavg | awk '{print $2}')
ONEMINUTE=$(cat /proc/loadavg | awk '{print $3}')
CPUS=$(grep -c processor /proc/cpuinfo)

# I/O INFO
BLOCKSIN=$(vmstat | tail -1 | awk '{print $9}')
BLOCKSOUT=$(vmstat | tail -1 | awk '{print $10}')
READSPERSEC=$(sar -b | tail -1 | awk '{print $5}')
WRITESPERSEC=$(sar -b | tail -1 | awk '{print $6}')

CPULINE="cpu,host=${HOSTNAME} user=${USER},system=${SYSTEM},idle=${IDLE},iowait=${IOWAIT},nice=${NICE}"
SWAPLINE="swap,host=${HOSTNAME} totalswap=${TOTALSWAP},freeswap=${FREESWAP},usedswap=${USEDSWAP}"
MEMLINE="memory,host=${HOSTNAME} totalmem=${TOTALMEM},freemem=${FREEMEM},cacheusage=${CACHEUSAGE},available=${AVAILABLE}"
LOADLINE="load,host=${HOSTNAME} cpus=${CPUS},fifteenminute=${FIFTEENMINUTE},fiveminute=${FIVEMINUTE},oneminute=${ONEMINUTE}"
IOLINE="iops,host=${HOSTNAME} bi=${BLOCKSIN},bo=${BLOCKSOUT},rps=${READSPERSEC},wps=${WRITESPERSEC}"

for LINE in "${CPULINE}" "${SWAPLINE}" "${MEMLINE}" "${LOADLINE}" "${IOLINE}"; do
  curl -i -XPOST "http://${INFLUXHOST}:8086/write?db=perf" --data-binary "${LINE}" >/dev/null 2>&1
done
