#!/bin/bash
chown user:user $1
mv $1 /data/dumped_pcap/$(date +%s%N).pcap
