#!/usr/bin/env bash
sudo socat pty,link=/dev/ttyTCP0,ignoreeof,user=will,group=dialout,mode=777,raw,echo=0 tcp:192.168.0.116:23