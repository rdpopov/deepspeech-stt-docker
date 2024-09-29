#!/usr/bin/bash

sudo netstat -ap | grep 9999 | awk -F'/' '{print $1}' |awk '{print $7}' |sort -u | grep "[0-9]" | xargs kill -9
