#!/bin/bash

INFLUXHOST=localhost
INFLUXDB=perf

# DATE/TIME for time series DB
TIMESTAMP=$(date +%s)

# HOSTNAME
HOSTNAME=$(hostname -s)

# CPU INFO
USER=$(vmstat | tail -1 | awk '{print $13}')
SYSTEM=$(vmstat | tail -1 | awk '{print $14}')
IDLE=$(vmstat | tail -1 | awk '{print $15}')
IOWAIT=$(vmstat | tail -1 | awk '{print $16}')

# SWAP INFO
TOTALSWAP=$(cat /proc/meminfo | grep SwapTotal | awk '{print $2'})
FREESWAP=$(cat /proc/meminfo | grep SwapFree | awk '{print $2'})
USEDSWAP=$(( ${TOTALSWAP} - ${FREESWAP} ))

# MEMORY INFO
TOTALMEM=$(cat /proc/meminfo | grep MemTotal | awk '{print $2'})
FREEMEM=$(cat /proc/meminfo | grep MemFree | awk '{print $2'})
CACHEUSAGE=$(cat /proc/meminfo | grep ^Cached | awk '{print $2'})

# LOAD INFO
FIFTEENMINUTE=$(cat /proc/loadavg | awk '{print $1}')
FIVEMINUTE=$(cat /proc/loadavg | awk '{print $2}')
ONEMINUTE=$(cat /proc/loadavg | awk '{print $3}')

# I/O INFO
BLOCKSIN=$(vmstat | tail -1 | awk '{print $9}')
BLOCKSOUT=$(vmstat | tail -1 | awk '{print $10}')
READSPERSEC=$(sar -b | tail -1 | awk '{print $5}')
WRITESPERSEC=$(sar -b | tail -1 | awk '{print $6}')

CPULINE="cpu,host=${HOSTNAME} user=${USER},idle=${IDLE},iowait=${IOWAIT} ${TIMESTAMP}"
SWAPLINE="swap,host=${HOSTNAME} totalswap=${TOTALSWAP},freeswap=${FREESWAP},usedswap=${USEDSWAP} ${TIMESTAMP}"
MEMLINE="memory,host=${HOSTNAME} totalmem=${TOTALMEM},freemem=${FREEMEM},cacheusage=${CACHEUSAGE} ${TIMESTAMP}"
LOADLINE="load,host=${HOSTNAME} fifteenminute=${FIFTEENMINUTE},fiveminute=${FIVEMINUTE},oneminute=${ONEMINUTE} ${TIMESTAMP}"
IOLINE="iops,host=${HOSTNAME} bi=${BLOCKSIN},bo=${BLOCKSOUT},rps=${READSPERSEC},wps=${WRITESPERSEC} ${TIMESTAMP}"

for LINE in "${CPULINE}" "${SWAPLINE}" "${MEMLINE}" "${LOADLINE}" "${IOLINE}"; do
  curl -i -XPOST 'http://localhost:8086/write?db=perf' --data-binary "${LINE}" >> influx.log 2>&1
done
