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
    echo `echo $1 | xxd -p -r | file -`  >> $(pwd)/test.o && echo `echo $1 | xxd -p -r | base64`  >> $(pwd)/test.o && echo `echo $1 | xxd -p -r | hexdump -C | base64`  >> $(pwd)/test.o;
    dump=`echo $1 | xxd -p -r | hexdump -C | xargs -0 -I {} echo -e "$(date +"%Y-%m-%d %T")\n"{} | text2pcap -d - - 2>/dev/null | tshark -V -Nn -T json -r -`
    fileType=`echo $1 | xxd -p -r | file -`
    decodeText=`echo $1 | xxd -p -r | iconv -f BIG5-HKSCS -t utf-8`
    if [ 0 -ne `echo ${dump} | grep -vw "\"frame.protocols\":\s\"\(eth\|eth:data\|eth:ethertype\|eth:ethertype:data\|eth:llc:data\)\"" | wc -l` ];
    then
        echo "[ ${dump} ]\n...";
    elif [ 0 -ne `echo ${dump} | grep -E "eth\.(dst\|src)_resolved\":\s\"([a-zA-Z0-9]{3,}(:|))+" | wc -l` ];
    then
        echo "[${dump}]\n...";
    fi
}

if [ -z "$@" ];
then
    exit 0;
else
    main $@
fi