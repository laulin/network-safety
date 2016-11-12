#FROM resin/rpi-raspbian
FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y tcpdump
RUN apt-get install -y tshark
RUN apt-get install -y supervisor
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump && \
    mkdir -p /data &&\
    pip3 install PyYAML inotify &&\
    useradd -ms /bin/bash user && mkdir -p /home/user && chown user:user /home/user

COPY configuration/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
COPY configuration/etc/probe.yaml /etc/probe.yaml
COPY sources/*.py /home/user/

RUN chmod a+r /etc/supervisor/conf.d/*.conf &&\
    chmod a+r /etc/probe.yaml &&\
    chmod a+rw /data &&\
    chown user:user /var/log/supervisor/

#USER user
WORKDIR /home/user/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
