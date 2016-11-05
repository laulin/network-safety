#FROM resin/rpi-raspbian
FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y tcpdump
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump
RUN apt-get install -y tshark
RUN apt-get install -y python3-yaml
# option
RUN apt-get install -y net-tools
RUN apt-get install -y supervisor
RUN apt-get install -y inotify-tools
RUN apt-get install -y vim

RUN mkdir /data
RUN mkdir /data/tmp_pcap
RUN mkdir /data/dumped_pcap

COPY configuration/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/

COPY sources/mv.sh /usr/bin/mv_pcap.sh

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
