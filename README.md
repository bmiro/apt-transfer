Tool install same packages on each computer you manage reducing the Internet
bandiwth creating local repositories.

The tool consist in two parts, the server part executed on the templete machine
that you want to clone the installed packages and the client to install all
the same packages that are on the server.

SCENARIO:

Imagine that you have a Debian-base computer class with diferent hardware
configurations. You want all the computers with the same software but due the
diferent hardware is difficult to use hard-disk cloning tools like CloneZilla[1].
Imagine also that you have limited Internet connection so you don't want to
re-download each packge on each machine. And you don't have a local server
so you can't use apt-cache-ng[2].

You want to install all the packages on one machine and then the others take
this packages from that one.

This tool also pretends to give a rapid way to setup a local mirror[3] for your
Debian-based distribution.


apt-transfer-server depends on:
    apt python3 apt-mirror

apt-transfer-client depends on:
    apt python3

Also if you want to use the gui you'll need pyqt4

[1] CloneZilla    http://clonezilla.org/ 
[2] apt-cache-ng  https://www.unix-ag.uni-kl.de/~bloch/acng/ 
[3] apt-mirror    http://apt-mirror.sourceforge.net/ 


bartomeumiro at gmail dot com, August 2012, Kathmandu - Nepal
