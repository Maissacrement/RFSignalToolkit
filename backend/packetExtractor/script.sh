#!/bin/bash

function main () {
    cat /tmp/set | text2pcap -d - - 2>/dev/null | tshark -V -Nn -T ek -Y \
        "(frame.protocols!=eth:ethertype:data and \
        frame.protocols!=eth:llc:data and \
        frame.protocols!=eth:data) or \
        (eth.src.oui_resolved or eth.src.oui_resolved)" \
    -r -
}

if [ -z "$@" ];
then
    exit 0;
else
    mkdir -p ./dumps;
    for dump in $@;do    /usr/bin/env echo ${dump} | od -Ax -tx1 -v >> /tmp/set;done
    main
fi