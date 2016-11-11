tcpdump -pni eth1 -B 10240 -s65535 -C 50 -G 60 -w '/mnt/usb/pcap/tmp/%s.pcap' -z /home/pi/mv.sh
