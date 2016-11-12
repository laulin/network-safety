#FROM resin/rpi-raspbian
FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y tcpdump
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tshark
RUN apt-get install -y supervisor
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump && \
    mkdir -p /data &&\
    pip3 install PyYAML inotify &&\
    useradd -ms /bin/bash user && mkdir -p /home/user && chown user:user /home/user &&\
    echo "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf" > /home/user/run.sh && chmod a+x /home/user/run.sh &&\
    echo "find /data/ | grep \\.csv$ | xargs rm ; find /data/ | grep \\.pcap$ | xargs rm" > /home/user/clear_all.sh && chmod a+x /home/user/clear_all.sh


COPY configuration/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
COPY configuration/etc/probe.yaml /etc/probe.yaml
COPY sources/*.py /home/user/

RUN chmod a+r /etc/supervisor/conf.d/*.conf &&\
    chmod a+r /etc/probe.yaml &&\
    chmod a+rw /data &&\
    chown user:user /var/log/supervisor/

WORKDIR /home/user/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
