import re
import os

hexToUri=lambda uri: '+'.join([ uri[i:i+2] for i in range(0, len(uri), 2) ])

curl=lambda hex: str(os.system("curl 'http://eon.sadjad.org/phd/' \
    -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    --compressed -H 'Referer: http://eon.sadjad.org/phd/' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Origin: http://eon.sadjad.org' \
    -H 'Connection: keep-alive'\
    -H 'Cookie: csrftoken=3f0d162c03c7abde71d11d9ef9195791; sessionid=0bcd70f89b0a979fe9946ebd32bc3079' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'Cache-Control: max-age=0' \
    --data-raw 'csrfmiddlewaretoken=3f0d162c03c7abde71d11d9ef9195791&packet={}' > dump.html".format(hex)))

cut=['Frame 1', 'Ethernet II', 'Data']

def packetHtmlToObject(htmlpacket):
    pos=[]
    frame={}
    these_regex="href=\"#\">(.+?)</a>"
    pattern=re.compile(these_regex)
    response=re.findall(pattern, ''.join(htmlpacket))
    for segment in cut:
        t=[ i if text.startswith(segment) else None for i, text in enumerate(response) ]
        t=[ *filter(lambda x: x != None, t) ]
        print(htmlpacket)
        pos.append(t[0])
    
    pos.append(t[len(t) - 1])

    for index in range(len(pos) - 1):
        frame[cut[index]]=response[pos[index]+1:pos[index+1]]

    return frame

def getFrame():
    with open('./dump.html', 'r') as dump:
        return packetHtmlToObject(dump)
