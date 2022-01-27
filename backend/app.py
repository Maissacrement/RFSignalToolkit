#!/usr/bin/env python3
from flask_cors import CORS,cross_origin
from flask import Flask, Response, request

from core.analyse import Analyse
from core.can import CAN
from core.udpAnalyser import UdPAnalyser
import matplotlib.pyplot as plt
from function.math1 import instanceSineWave
from function.dataframes import magnet, convertToMagnet
import struct
import json
import os
import numpy as np
import function.packetReader as packet
import os
import pandas as pd
import sys
import subprocess

def extractor(dumplist):
    print('searching..')
    try:
        print(dumplist)
        dumplist=[ *filter(lambda x: len(x.strip()) != 0, dumplist) ]
        for i, dt in enumerate(dumplist):
            packet=subprocess.run(["{}/packetExtractor/script.sh".format(os.getcwd()), str(dt)], capture_output=True)
            if packet.returncode == 0 and len(packet.stdout) != 0:
                formatPacket=packet.stdout[:len(packet.stdout) - 8]
                print(formatPacket)
                yield packet.stdout
            #os.system('./packetExtractor/script.sh {}'.format(dt))
            #if os.path.getsize("./debug.json"):
            #    with open('./debug.json', 'rb') as debug:
            #        yield debug.read()
    finally:
        print("End")
                

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/dynmagnet', methods=['POST', 'GET'])
def dyns():
    MTU=1125# 1125 octet --> 9000 byte Jumbo ?
    #df = pd.DataFrame({})
    analyse = Analyse()
    signal = None
    dumpShiftedLeft=[]
    i = 2400
    df=convertToMagnet(request.get_json())
    
    sig=[]
    FREQUENCY=60000
    if(len(sys.argv) > 1):
        FREQUENCY=int(sys.argv[1])

    print('[APP]: is running for {} Mhz'.format(FREQUENCY))

    # Search from frequency range 1000000000 hertz to 900000000000 hertz
    cut=int(len(df)/MTU)
    for j in range(cut):
        analyse.provideDataset(False, df[j:]) if len(df[j:]) < MTU else analyse.provideDataset(False, df[j:j+MTU])
        #analyse.provideDataset(False, df[0:])
        signal = analyse.changeFrequency( FREQUENCY )
        print(signal)
        if signal:
            numericalAnalysis=CAN()
            s=numericalAnalysis.qbits(numericalAnalysis.can(15, signal[1][1:].real))
            if(s not in sig):
                p=''.join(s)
                sig.append(p)
                dumpShiftedLeft+=[p] +[ ''.join([ hex(int(p[x:x+2], 16) ^ i)[2:] for x in range(int(len(p) / 2)) ]) for i in range(127) ]

    return Response(extractor(dumpShiftedLeft), mimetype="application/json")
                    

    #else:
    #    return json.dumps({ "state": "null" })

@app.route('/magnet', methods=['POST'])
def push():
    #analyse = Analyse()
    #udp=UdPAnalyser()
    #analyse.provideDataset(os.getcwd() +'/json/radio.csv')
    #signal = analyse.changeFrequency(30)
    #s=''
    #if signal:
    #    numericalAnalysis=CAN()
    #    signal=[numericalAnalysis.can(16, signal[1].real), numericalAnalysis.can(16, signal[1].imag)]
    #    s=numericalAnalysis.qbits(signal[0])

    return json.dumps({
        'magnet': [magnet(req, mode = 'w' if i == 0 else 'a', filename='./radio.csv') for i, req in enumerate(request.get_json())],
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")