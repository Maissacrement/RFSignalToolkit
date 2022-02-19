#!/usr/bin/env bash
ids=$(uuidgen)
dts=$(date +%m_%d_%Y)
mkdir -p /tmp/location/$(dts)
touch /tmp/location/$(dts)/$(ids).json
for ip in $(cat $1 | xxd -p -r | strings -a | od -Ax -tx1 -v | text2pcap -m64 -i4  -d - - 2>/dev/null | tshark -tad -r - | grep -v Bogus | awk '{ print $4 }{ print $6 }');
do
    echo ${ip} `geoiplookup ${ip}` | grep -v "can't" | awk '{ print $1 }' | xargs -i curl https://ipinfo.io/{} >> /tmp/data.json 2>/dev/null; # /tmp/location/$(dts)/$(ids).json
done