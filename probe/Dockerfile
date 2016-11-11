FROM resin/rpi-raspbian
#FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y \
  python3\
  python3-pip\
  tcpdump\
  tshark\
  supervisor\
  inotify-tools &&\
  mv /usr/sbin/tcpdump /usr/bin/tcpdump && \
  mkdir -p /data /data/tmp_pcap /data/dumped_pcap

COPY configuration/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
COPY sources/mv.sh /usr/bin/mv_pcap.sh
COPY sources/pcap_to_csv.sh /usr/bin/pcap_to_csv.sh
COPY sources/pcap_to_csv_notify.sh /usr/bin/pcap_to_csv_notify.sh

RUN pip3 install PyYAML &&\
  useradd -ms /bin/bash user && mkdir -p /home/user && chown user:user /home/user &&\
  chmod a+r /etc/supervisor/conf.d/*.conf &&\
  echo "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf" > /home/user/run.sh && chmod a+x /home/user/run.sh &&\
  echo "find /data/ | grep \\.csv$ | xargs rm ; find /data/ | grep \\.pcap$ | xargs rm" > /home/user/clear_all.sh && chmod a+x /home/user/clear_all.sh &&\
  chown user:user /var/log/supervisor/

WORKDIR /home/user/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
