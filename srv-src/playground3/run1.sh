#!/usr/bin/bash

sudo netstat -ap | grep 9999 | awk -F'/' '{print $1}' |awk '{print $7}' |sort -u | grep "[0-9]" | xargs kill -9

python3 ./server.py &
python3 ./client.py 1 &

# for i in {0..1}; do 
#     # echo $i
#     python3 client.py $i &
# done

wait
