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

# SIGNAL FREQUENCY TYPE
signalRange={
  'bluetooth': [.00001, .00002, .0001, 2400, 2483.5, 60000, 200000, 600000],
  'wimax': [10000, 66000, 2000, 11000],
  'lorawan': [433.05, 434.79, 863, 870, 902.3, 914.9],
  'wifi': [900, 2.4 * (10**3), 3.6 * (10**3), 4.9 * (10**3), 5 * (10**3), 5.9 * (10**3), 6 * (10**3), 60 * (10**3)],
  'manet': [300  * (10**3)],
  'other': [9.20  * (10**3)]
}

wireless=[]
[ wireless.extend(x) for x in map(lambda x: signalRange.get(x), signalRange.keys()) ]

def extractor(dumplist, count):
    print('searching..')
    os.system('echo > /tmp/set;')
    try:
        dumplist=[ *filter(lambda x: len(x.strip()) != 0, dumplist) ]
        for i in range(count - 1):
            dump=" ".join(dumplist[i*count:(1+i)*count])
            packet=subprocess.run(["{}/packetExtractor/script.sh".format(os.getcwd()), str(dump) ], stdout=subprocess.PIPE)
            if packet.returncode == 0:
                if (i == count -2): yield bytes(str(packet.stdout).encode('utf-8'))
    finally:
        print("End")
                

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/dynmagnet', methods=['POST', 'GET'])
def dyns():
    MTU=800# 1125 octet --> 9000 byte Jumbo ?
    analyse = Analyse()
    signal = None
    dumpShiftedLeft=[]
    i = 2400
    df=convertToMagnet(request.get_json())
    cut=int(len(df)/MTU)
    sig=[]

    # Search from frequency range 1000000000 hertz to 900000000000 hertz
    for FREQUENCY in wireless:
        print('[APP]: is running for {} Mhz'.format(FREQUENCY))
        for j in range(cut):
            analyse.provideDataset(False, df[j:]) if len(df[j:]) < MTU else analyse.provideDataset(False, df[j:j+MTU])
            signal = analyse.changeFrequency( FREQUENCY )
            if signal:
                numericalAnalysis=CAN()
                s=numericalAnalysis.qbits(numericalAnalysis.can(15, signal[1].real))
                if(s not in sig):
                    p=''.join(s)
                    sig.append(p)
                    dumpShiftedLeft+=[p] +[ ''.join([ hex(int(p[x:x+2], 16) ^ i)[2:] for x in range(int(len(p) / 2)) ]) for i in range(127) ]

    return Response(extractor(dumpShiftedLeft, cut), mimetype="application/json")
                    

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