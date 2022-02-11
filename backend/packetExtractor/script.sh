#!/bin/bash
function main () {
    text2pcap -m1125 -d $1 - 2>/dev/null | mergecap -w /tmp/set.pcap -
    rm -f $1 2>/dev/null &;
    tshark -2 -V -Nn -T ek -Y \
        "(frame.protocols!=eth:ethertype:data and \
        frame.protocols!=eth:llc:data and \
        frame.protocols!=eth:data) or \
        (eth.src.oui_resolved or eth.src.oui_resolved)" \
    -r /tmp/set.pcap;
}

if [ -z "$@" ];
then
    exit 0;
else
    fileid=/tmp/set$(uuidgen);
    touch ${fileid};
    mkdir -p ./dumps;
    for dump in $@;do    /usr/bin/env echo ${dump} | od -Ax -tx1 -v >> ${fileid};done
    main ${fileid};
fi