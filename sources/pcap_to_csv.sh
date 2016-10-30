while read line
do
    echo $line
    tshark -r $line -T fields -e frame.len -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e frame.protocols -E header=y -E separator=, -E quote=d > /mnt/usb/pcap/csv/$(date +%s%N).csv
    rm -f $line
done

# tshark -i br0 -T fields -e frame.len -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e frame.protocols -E header=y -E separator=, -E quote=d
#tshark -i br0 -T fields -e frame.len -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e frame.protocols -Y "not ip.addr==192.168.0.251"
