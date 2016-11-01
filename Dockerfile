FROM resin/rpi-raspbian

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y tcpdump
RUN apt-get install -y tshark
RUN apt-get install -y python3-yaml
RUN apt-get install -y net-tools

RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump
