#!/bin/bash
cat ./res | xxd -p -r | od -Ax -tx1 -v | text2pcap -i4 - - 2>/dev/null | tshark -r - -w - >> ./bin.pcap &
tshark -T json -2 -r ./bin.pcap -Y \
    "(frame.protocols!=eth:ethertype:data and \
    frame.protocols!=eth:llc:data and \
    frame.protocols!=eth:llc and \
    frame.protocols!=eth:data)" \
2>/dev/null 
#file=`cat $1 | od -Ax -tx1 -v`
#echo -e "$file\n*"
#| text2pcap -d - - 2>/dev/null | tshark -x -r -  2>/dev/null