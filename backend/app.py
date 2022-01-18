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

def extractor(dumplist):
    for dt in dumplist:
        os.system('./packetExtractor/script.sh {}'.format(dt))
        if os.path.getsize("./debug.json"):
            with open('./debug.json', 'rb') as debug:
                yield bytes(debug.read())
                

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

    df=convertToMagnet(request.get_json() * 50)
    
    sig=[]
    app=[]

    # Search from frequency range 1000000000 hertz to 900000000000 hertz
    cut=int(len(df)/MTU)
    for j in range(cut):
        analyse.provideDataset(False, df[j:]) if len(df[j:]) < MTU else analyse.provideDataset(False, df[j:j+MTU])
        #for i in range(60000, 94000, 1000):
        signal = analyse.changeFrequency(60000)
        if signal:
            numericalAnalysis=CAN()
            s=numericalAnalysis.qbits(numericalAnalysis.can(15, signal[1][1:].real))
            if(s not in sig):
                sig.append(s)
                p=''.join(s)
                dumpShiftedLeft+=[p] +[ ''.join([ hex(int(p[x:x+2], 16) ^ i)[2:] for x in range(int(len(p) / 2)) ]) for i in range(127) ]

    return Response(extractor(dumpShiftedLeft), mimetype="application/json")
                    

    #else:
    #    return json.dumps({ "state": "null" })

@app.route('/magnet', methods=['POST'])
def push():
    analyse = Analyse()
    udp=UdPAnalyser()
    analyse.provideDataset(os.getcwd() +'/json/radio.csv')
    signal = analyse.changeFrequency(30)
    s=''

    if signal:
        numericalAnalysis=CAN()
        signal=[numericalAnalysis.can(16, signal[1].real), numericalAnalysis.can(16, signal[1].imag)]
        s=numericalAnalysis.qbits(signal[0])

    return json.dumps({
        'magnet': [magnet(req, mode = 'w' if i == 0 else 'a', filename='./radio.csv') for i, req in enumerate(request.get_json())],
        'dump': udp.dump(s)
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")