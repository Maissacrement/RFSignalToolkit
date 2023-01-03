#!/bin/bash
####### EXTRACT IP FROM BINARY FILE ###########
file=$1
cat $(ls $file | grep -v .pcap) | text2pcap -l228 -m128 -d - - 2>/dev/null | tshark -r - | grep -v "Bogus\|Malformed" | awk '{ print $3 }{ print $5 }'