inotifywait -rme move --format '%w%f' --exclude "/$" /mnt/usb/pcap/dumped/ | ~/pcap_to_csv.sh
