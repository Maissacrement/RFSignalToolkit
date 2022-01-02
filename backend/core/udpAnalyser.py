import struct
import hexdump
import binascii
from pylibpcap import wpcap
import json
import codecs

pdu3gpp = {
  "0": "DL USER DATA",
  "1": "DL DATA DELIVERY STATUS",
  "2": "DL DATA DELIVERY STATUS EXTENDED",
  "3": "DL USER DATA EXTENDED",
  "4-15": "reserved for future PDU type extensions"
}

class UdPAnalyser:
    
    # Decode data
    def xor_strings(self, xs, ys):
        return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

    def decodeData(self, chain):
        parsedChain = ''
        decode=lambda x, y="98": codecs.encode(bytes(self.xor_strings(x, y).encode('utf-7')), "hex")
        for i in range(0, len(chain), 2):
            tmp = decode(chain[i:i+2])
            for tmpIndex in range(0, len(tmp), 2):
                parsedChain+=chr(int(tmp[tmpIndex:tmpIndex+2], 16))

        return parsedChain

    def hexToStr(self, data):
        data=data.decode()
        return ' '.join(str(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

    def hexToIp(self, ip):
        return ':'.join(ip[i:i+2] for i in range(0, len(ip), 2))

    def unpack3GPP(self, data):
        #pdu=bytearray(data.encode('utf-8'))
        x={
            "header": {
              "version": data[0:4],
              "dscp": data[4:8],
              "flowLabel": data[10:16],
              "payloadLength": data[16:24],
              "NxtHdr": data[24:28],
              "hop": data[28:32],
            },
            "address": {           
                "src": str(self.hexToIp(data[32:48])),
                "dst": self.hexToIp(data[48:64]),
            },
            "data": self.decodeData(data[64:]).format()
        }
        return json.dumps(x, indent=4)


    def dump(self, buffer, fmt="! 8s 8s 2s", size=16):
        buffer=''.join(buffer)
        tab=[]
        tab.append(self.unpack3GPP(buffer[0:]))

        return tab
            

"""
udp=UdPAnalyser()
arr=['aa', 'ba', 'ca', '1a', '1a', 'aa', 'aa', 'aa', 'ba', 'aa', 'ba', 'ca', 'aa', 'ba', 'aa', 'aa']

fmt= "! 8s 8s" # > work for 16 bit arr
size = struct.calcsize(fmt)

udp.dump(arr, fmt=fmt, size=size)
"""



"""
if(len(buffer) > 48):
    frameID=int(buffer[32:48], 16)
while len(buffer[frameID+32:]) - frameID < 0 and len(buffer[frameID+32:]) > 16:
    tab.append(self.unpack3GPP(buffer[:frameID]))
    print(tab)
    frameID+=int(buffer[frameID+32:frameID+48], 16)
if len(buffer[frameID+32:]) > 16:
    frameID+=int(buffer[frameID+32:frameID+48], 16)
""" 

#[ print(self.unpack3GPP(buffer[32*i:32*i+32])) for i in range(int(len(buffer) / 32)) ]
#buffer=bytearray([ int(bin(int(buffer[x*2:(x*2)+2], 16)), 2) for x in range(int(len(buffer) /2)) ])
   
#hexdump.hexdump( buffer )
#wpcap(buffer, "pcap.pcap")
"""
with open('test.cap', 'ab') as cap:
    td=''.join([ chr(int(bin(int(el, base=16))[2:], 2)) for el in buffer ]).encode('utf-8')
    cap.write(bytes(td))
    i=bytearray(''.join(buffer).encode('utf-8'))
    print(i)
    print(struct.unpack("!6H4s4s", i[:20]))
    dest, src, prototype, *data = struct.unpack('! 6H4s4s', i[:20])
    print( dest )
    # prototype=binascii.hexlify(int(prototype, 16))
    print( 'dest: ', dest, '\nsrc: ', src, '\nprototype: ', prototype, '\nd: ', data )
    (ip, src) = struct.unpack(fmt, i[:size])
    print( self.hexToIp( ip ) )
    print( self.hexToIp( src ) )
cap.close()
"""