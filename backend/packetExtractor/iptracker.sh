#!/usr/bin/env bash
# ids=$(uuidgen)
# dts=$(date +%m_%d_%Y)
# mkdir -p /tmp/location/$(dts)
# touch /tmp/location/$(dts)/$(ids).json
for ip in $(cat $(ls $1* | grep -v ".pacp") | text2pcap -m32 -i4  -d - - 2>/dev/null | tshark -r - | grep -v Bogus | awk '{ print $3 }{ print $5 }');
do
    echo ${ip} `geoiplookup ${ip}` | grep -v "can't" | grep France | awk '{ print $1 }' | xargs -i curl https://ipinfo.io/{} 2>/dev/null; # /tmp/location/$(dts)/$(ids).json
done