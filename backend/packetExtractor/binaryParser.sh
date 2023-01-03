#!/usr/bin/env bash
ids=$(uuidgen)
dts=$(date +%m_%d_%Y)
mkdir -p /tmp/location/$(dts)
touch /tmp/location/$(dts)/$(ids).txt
for data in `echo $1 | xxd -p -r`;
do
    typestr=`echo $data | xxd -p -r | chardetect3 /dev/stdin 2>/dev/null | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no\|empty/UNICODE/g`;
    deep-translator --source "auto" --target "en" --tex "$(echo $data | iconv -c -f $typestr -t utf-8 -s 2>/dev/null | iconv -c -f unicode -t BIG5-HKSCS -s 2>/dev/null | iconv -c -f unicode -t utf-8 -s 2>/dev/null)" 2>/dev/null | grep "Translation result: " | cut -d ':' -f2 | trans :en -b -e aspell | od -An -tx1 -v | xxd -p -r >> /tmp/data_translated; #location/$(dts)/$(ids).txt
done

#function typeParserLoop () {
#    i=$1
#    if echo $i | file - | grep nicode
#    then
#        typeParserLoop $(echo $i | iconv -f $(echo $i | chardetect3 /dev/stdin | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no/UNICODE/g) -t utf-8);
#    elif echo $i | file - | grep UTF-8
#    then
#        trans -e yandex -b;
#    fi
#}
#
#translator () {
#    d=$1
#    typestr=`echo $d | chardetect /dev/stdin 2>/dev/null | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no\|empty/UNICODE/g`
#    deep-translator --source "auto" --target "en" --tex "$(echo $data | iconv -c -f $typestr -t utf-8 -s 2>/dev/null | iconv -c -f unicode -t BIG5-HKSCS -s 2>/dev/null | iconv -c -f unicode -t utf-8 -s 2>/dev/null)" 2>/dev/null
#    
#    #typestr=`echo $d | chardetect /dev/stdin 2>/dev/null | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no\|empty/UNICODE/g`;
#    #binary=`echo $d | iconv -c -f $typestr -t utf-8 -s 2>/dev/null`;
#    #if echo $binary | file - 2>/dev/null | grep -w 'nicode\|text';then
#    #    if echo $binary | echo chardetect /dev/stdin 2>/dev/null | grep -v "utf-8\|ascii" >/dev/null;then
#    #        echo $d | iconv -c -f unicode -t UTF-8 -s 2>/dev/null | trans :fr -b
#    #        #translator "$(echo $binary | iconv -c -f $typestr -t utf-8 -s 2>/dev/null | strings -a)"
#    #    else
#    #        echo $d | iconv -c -f unicode -t UTF-8 -s 2>/dev/null | trans :fr -e google -b
#    #    fi
#    #else
#    #    echo $d
#    #fi
#}
#
#touch /tmp/data_translated /tmp/data
##$(cat ./test | od -Ax -tx1 -v | text2pcap -m64 -i4  -d - - 2>/dev/null | tshark -tad -r - -x | xxd -p -r)
#payloads=$(cat ./test | od -Ax -tx1 -v | text2pcap -m64 -i4  -d - - 2>/dev/null | tshark -tad -r - -x | xxd -p -r)
#for data in $payloads;
#do
#    typestr=`echo $data | xxd -p -r | chardetect3 /dev/stdin 2>/dev/null | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no\|empty/UNICODE/g`;
#    deep-translator --source "auto" --target "fr" --tex "$(echo $data | iconv -c -f $typestr -t utf-8 -s 2>/dev/null | iconv -c -f unicode -t BIG5-HKSCS -s 2>/dev/null | iconv -c -f unicode -t utf-8 -s 2>/dev/null)" 2>/dev/null | grep "Translation result: " | cut -d ':' -f2 | trans :en -b -e aspell
#done
#
#for i in $(cat $(ls -la /tmp | grep "14 22:" | grep -v ".pcap" | awk '{ print $9 }') | xxd -p -r | strings -a | od -Ax -tx1 -v | text2pcap -m64 -i4  -d - - 2>/dev/null | tshark -tad -r - -x | xxd -p -r);do     if echo $i | file - | grep nicode;then    echo $i | iconv -f $(echo $i | chardetect3 /dev/stdin | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no/UNICODE/g) -t utf-8 | trans :fr -e aspell -b;fi; done
#type=$(echo $d | chardetect /dev/stdin | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no\|empty/UNICODE/g)
#echo $d | strings -d | iconv -c -f $type -t utf-8  2>/dev/null | file -
#echo $d | strings -d | iconv -c -f $type -t utf-8  2>/dev/null
#cat ./u.o | xxd -p -r | iconv -f UTF-16LE -t UTF-8
#for i in $dumparsed;
#do
#    echo $i
#    if echo $i | file - | grep nicode
#    then
#        echo $i | iconv -f $(echo $i | chardetect /dev/stdin | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no/UNICODE/g) -t utf-8 | trans :fr -e aspell -b;
#    fi
#done
exit 0

touch ./encodfile
echo ${data} > ./encodfile
file -i ./encodfile
iconv -f -c utf-8 -t utf-8 ./encodfile -o ./encodfile 2>/dev/null
recode --sequence=memory -f utf-8 ./encodfile
strings ./encodfile