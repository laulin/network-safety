FROM resin/rpi-raspbian
#FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y \
  python3\
  tcpdump\
  tshark\
  python3-yaml\
  supervisor\
  inotify-tools\
  net-tools && \
  mv /usr/sbin/tcpdump /usr/bin/tcpdump && \
  mkdir -p /data /data/tmp_pcap /data/dumped_pcap

RUN useradd -ms /bin/bash user && mkdir -p /home/user && chown user:user /home/user

COPY configuration/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
RUN chmod a+r /etc/supervisor/conf.d/*.conf

COPY sources/mv.sh /usr/bin/mv_pcap.sh
COPY sources/pcap_to_csv.sh /usr/bin/pcap_to_csv.sh
COPY sources/pcap_to_csv_notify.sh /usr/bin/pcap_to_csv_notify.sh
RUN echo "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf" > /home/user/run.sh && chmod a+x /home/user/run.sh
RUN echo "find . | grep \\.csv$ | xargs rm ; find . | grep \\.pcap$ | xargs rm" > /home/user/clear_all.sh && chmod a+x /home/user/clear_all.sh

RUN chown user:user /var/log/supervisor/
WORKDIR /home/user/

#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
