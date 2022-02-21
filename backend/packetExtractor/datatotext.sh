typestr=`echo $1 | chardetect /dev/stdin 2>/dev/null | xargs -i echo {} | awk '{ print $2 }' | sed -E s/no\|empty/UNICODE/g`; 
deep-translator --source "auto" --target "fr" --tex "$(echo $1 | iconv -c -f $typestr -t utf-8 -s 2>/dev/null | iconv -c -f unicode -t BIG5-HKSCS -s 2>/dev/null | iconv -c -f unicode -t utf-8 -s 2>/dev/null)" 2>/dev/null | grep "Translation result: " | cut -d ':' -f2 | trans :fr -b -e aspell | od -An -tx1 -v | xxd -p -r;