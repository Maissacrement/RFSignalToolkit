#!/bin/bash
function main () {
    #${PWD}/packetExtractor/datatotext.sh `cat $1`
    #${PWD}/packetExtractor/fastDecodeTest.sh `cat $1`
    protocols="6 1 4 21 3 8 9 78 79 119"
    touch /tmp/set.pcap $1.pcap
    cat $1 >> /tmp/set
    for proto in ${protocols};do
        text2pcap -m24 -i${proto} -d $1 $1.pcap 2>/dev/null;
        cat /tmp/set.pcap | mergecap -I all -a -w /tmp/set.pcap $1.pcap - 2>/dev/null;
    done
    text2pcap -d $1 $1.pcap 2>/dev/null;
    cat /tmp/set.pcap | mergecap -I all -a -w /tmp/set.pcap $1.pcap - 2>/dev/null;
    #tshark -2 -V -Nn -T ek 
    tshark -2 -r /tmp/set.pcap -V -T ek -Y \
        "(frame.protocols!=eth:ethertype:data and \
        frame.protocols!=eth:llc:data and \
        frame.protocols!=eth:data) or \
        (eth.src.oui_resolved or eth.src.oui_resolved)" \
    2>/dev/null | grep -v "index\|malformed";
    rm -vf $1.pcap;
}

if [ $# -le 1 ];
then
    exit 0;
else
    chmod +x ${PWD}/packetExtractor/*.sh
    touch /tmp/set
    fileid=/tmp/set$(uuidgen);
    touch ${fileid};
    mkdir -p ./dumps;
    for dump in $@;do    /usr/bin/env echo ${dump} | xxd -p -r | od -Ax -tx1 -v >> ${fileid};done
    main ${fileid};
fi