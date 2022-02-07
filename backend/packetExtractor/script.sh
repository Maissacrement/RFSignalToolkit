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

    #cat /tmp/set | text2pcap -d -m1460 -i4 - - 2>/dev/null | tshark -V -Nn -T json -r -;
    #/usr/bin/env echo {} | xxd -p -r | hexdump -C | text2pcap -d -m1460 -i4 - - 2>/dev/null |  tshark -V -Nn -T  -r -
    #10.1.1.1\|10.2.2.2\|IPv4 total length exceeds\|Bogus
    #echo $1 | xxd -p -r | hexdump -C | text2pcap -d - - | tcpdump -nvvvX -
    #echo `echo $1 | xxd -p -r | file -`  >> $(pwd)/test.o && echo `echo $1 | xxd -p -r`  >> $(pwd)/test.o && echo `echo $1 | xxd -p -r | hexdump -C`  >> $(pwd)/test.o;
    #dump=`echo $1 | xxd -p -r | hexdump -C | xargs -0 -I {} echo -e "$(date +"%Y-%m-%d %T")\n"{} | text2pcap -d - - 2>/dev/null | tshark -V -Nn -T json -x -r -`
#
    ##fileType=`echo $1 | xxd -p -r | file -`
    ##decodeText=`echo $1 | xxd -p -r | iconv -f BIG5-HKSCS -t utf-8`
    #if [ 0 -ne `echo ${dump} | grep -vw "\"frame.protocols\":\s\"\(eth\|eth:data\|eth:ethertype\|eth:ethertype:data\|eth:llc:data\)\"" | wc -l` ];
    #then
    #    echo "[ ${dump} ]\n...";
    #    echo $1 | xxd -p -r | hexdump -C | text2pcap -d - - | tcpdump -AvXX -ttttnnr -
    #elif [ 0 -ne `echo ${dump} | grep -E "eth\.(dst\|src)_resolved\":(\s|\t)+\"([a-zA-Z0-9]{3,}(:|))+" | wc -l` ];
    #then
    #    echo "[${dump}]\n...";
    #fi
}

function main () {
    cat /tmp/set/$1 | text2pcap -d - - 2>/dev/null | tshark -V -Nn -T ek -Y \
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
    echo /tmp/set
    for dump in "${@:2:$#}";do    /usr/bin/env echo ${dump} | xxd -p -r | hexdump -C >> /tmp/set;done
    main $2
fi