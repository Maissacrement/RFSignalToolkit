#!/bin/bash
file=$1
cat $(ls $file | grep -v .pcap) | text2pcap -m32 -i4 -d - - 2>/dev/null | tshark -r - | grep -v "Bogus\|Malformed" | awk '{ print $3 }{ print $5 }' | sort -un | uniq