#FROM resin/rpi-raspbian
FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /tmp

RUN apt-get update -y && apt-get install -y python3 python3-pip
RUN apt-get install -y wget
RUN wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
RUN bash Anaconda3-4.2.0-Linux-x86_64.sh -b
RUN useradd -ms /bin/bash user && mkdir -p /home/user && chown user:user /home/user
run mkdir -p /data && chown user:user /data
EXPOSE 8888

USER user
WORKDIR /home/user/

CMD ["jupyter"]
