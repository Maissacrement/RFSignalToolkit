#!/bin/sh
file=/tmp/set.pcap
enc=UTF-7
touch ${file}
cat ${file} | xxd -p -r | iconv -f UNICODE -t $enc | iconv -f $enc -t UTF-8 >> /tmp/data.log