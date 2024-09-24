#!/usr/bin/bash

python3 ./server.py &
python3 client.py 1 &

# for i in {0..5}; do 
#     # echo $i
#     python3 client.py $i &
# done

wait
