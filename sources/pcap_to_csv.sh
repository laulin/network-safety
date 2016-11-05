#!/bin/bash
while read line
do
    echo $line
    mkdir -p /data/csv/$(date +%F)
    tshark -r $line -T fields -e frame.len -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e frame.protocols -E header=y -E separator=, -E quote=d > /data/csv/$(date +%F)/$(date +%s%N).csv
    rm -f $line

done
