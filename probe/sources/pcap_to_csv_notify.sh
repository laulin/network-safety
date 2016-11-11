#!/bin/bash
inotifywait -rme move --format '%w%f' --exclude "/$" /data/dumped_pcap/ | /usr/bin/pcap_to_csv.sh
