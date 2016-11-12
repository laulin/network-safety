# network-safety

## Why ?

One day, while I watched my router's led blinking, I just wondered "What is
happening on my wire ?"

From this point, I decided to check it by my self. And now my goal is to give
you a simple but powerful tool to monitor you network again malicious behavious
and emerging threats.

It is composed of two containers :

* probe : it captures network traffic and convert it into CSV file
* analytics : it takes CSV file and process it.

The analytics is not currently working but it is planned.

## Global warnings

You must be aware of what you are doing. **In any case I could not be held
responsible**. In particulary, you should be aware of :

* The probe will store all data available on the wire and it converts it into
metadata. It means you can see things and stuffs you *would not had seen*.
Even if many data are today ciphers, dns are not so porn sites or extra marital
dating sites will be stored.
* In some country, doing that may be ***illegal***.
* This probe was designed to be cheap and easy to do. I don't think it can
manage 100 Mbs network at full speed.
* Even experts may miss attacks on a network so do not imagine that an
algorithm is perfect. *The better protection you may have is yourself !*

You have been warned, so now let's play :)

## Hardware

At first you must have this stuff :

* a raspberry pi 3 board (I hadn't tested other board)
* a 16 Gb board
* a good - reliable - power supply
* two usb to ethernet adapters
* optionnal but highly recommanded : a usb key or an usb hard drive

You shouldn't **NOT** use the SD card as a storage. It is very slow, unefficient
and you will dramatically decrease its life time.

## Installation

### Os installation

I am using [Rasbian lite](https://www.raspberrypi.org/downloads/raspbian/) and
the installation process is well explained.

A good tips is about booting without HDMI : set hdmi_force_hotplug=1 in
config.txt before insert it.

By default, ssh is enable with user=*pi* and password=*raspberry*.

### Automatic installation

I try to make thing as easy as possible. I use Docker but I would also need to
use Ainsible the front line installation.

I will do in a future. Sorry.

### network capture

Many strategies exist - in your case - to capture the traffic :

* TAP (Test Acces Point) : on you internet connection, you can put a TAP that
copy bit by bit data on the wire. DIY version can me found
[here](http://lmgtfy.com/?q=tap+network+diy). Warning : this type of equipment
may be classifed as weaponary in some country !

* Bridge : by using two network interfaces you make an almost transparent
connection.

* Routing : About the same as bridge bu not transparent; using iptable you
can add rules for routing and even rules to protect you network
(see IDS vs IPS).

* Port mirroring : some routers can make
[port mirroring](https://en.wikipedia.org/wiki/Port_mirroring)

For my needs, I decided to use bridge version. It is the simplest in this case
and do not need specific stuff. You can test other configuration if you are
curious (IMO it's very interesting !).

So how to make a network bridge ? At first plug both USB to
ethernet adapters; Then *ifconfig* : you should
see eth0, eth1 and eth2, at least. At last, do :

* install bridge-utils
* add this to /etc/network/interfaces :
>     auto br0
>     iface br0 inet dhcp
>     bridge_ports eth1 eth2
>     bridge_stp off
>     bridge_waitport 0
>     bridge_fd 0
>     bridge_maxwait 0

* service network restart
* check that br0 is existing with *ifconfig*

Now you can man-in-the-middle you internet traffic. Check that you still have
an internet connection.

### Optionnal : mount storage

As I explained in the hardware listing, you should have an
external storage. In my case I use an USB key - not the best choice - as
storage. To mount it, I do :

* mkdir /data
* Add to /etc/fstab :

>/dev/sda1 /data/ ext4 defaults 0 0

You can also make a *SSHFS* to a NAS for example if you want. I love *SSHFS*.
A great thank you to *SSHFS* team - you make my day every day.

### I need a Whale

You need to install docker. For that, as root :

* wget on https://get.docker.com/
* run the script
* gpasswd -a pi docker
* service docker restart
* logout and login as pi

### Installing containers

A makefile should be added to make it easier. For both components, go to its
directory and *docker build -it {probe,analytics} .*.

You can clone on you desktop or on raspberry directory but do not try to build
an image on you desktop ("oh great, i will use docker {load,save}" - Nope) :
the instruction set (ARM vs X86) is different. You will have to build it on
you raspberry and it takes many time !

## Running it

### Probe

It is quiet easy :

>     docker run -d -p 9001:9001 --cap-add=NET_ADMIN --net=host -v /data:/data -it probe

Now on 127.0.0.1:9001, you can watch the supervisor interface : both capture
and process is running.

The directory /data/csv/yyyy-mm-dd/ will contains .csv file.

### Analytics

***TODO***
