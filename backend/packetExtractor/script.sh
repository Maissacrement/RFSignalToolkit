#!/bin/bash

mkdir -p ./dumps 

function main0 () {
    rm ./debug.json;touch ./debug.json
    file=dumps/res$(date +%s)$1
    date +"%Y-%m-%d %T" > ./${file}.txt 2>/dev/null
    echo $2 | xxd -p -r | hexdump -C >> ./${file}.txt 2>/dev/null
    text2pcap ./${file}.txt ./${file}.pcap 2>/dev/null && rm -vf ./${file}.txt &>/dev/null
    dump=`tshark -r ./${file}.pcap -V | jq  --raw-input .`
    echo ${dump} | jq --slurp . >> ./json/dump.json # Temp data for debug
    if [ 0 -ne `echo ${dump} | grep -v 'Protocols in frame: eth:ethertype:data' | wc -l` ];
    then
        echo create ./${file}.pcap
        echo ${dump} | jq --slurp . > ./debug.json
    else
        rm -vf ./${file}.pcap &>/dev/null
    fi
}

function main () {
    cat /tmp/set | text2pcap -d - - 2>/dev/null | tshark -V -Nn -T ek -Y \
        "(frame.protocols!=eth:ethertype:data and \
        frame.protocols!=eth:llc:data and \
        frame.protocols!=eth:data) or \
        (eth.src.oui_resolved or eth.src.oui_resolved)" \
    -r -
}

if [ -z "$#" ];
then
    exit 0;
else
    echo > /tmp/set
    for dump in "$@";do    /usr/bin/env echo ${dump} | xxd -p -r | hexdump -C >> /tmp/set;done
    main
fi