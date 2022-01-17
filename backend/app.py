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


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/dynmagnet', methods=['POST', 'GET'])
def dyns():
    df = pd.DataFrame({})
    analyse = Analyse()
    signal = None
    i = 1

    df=convertToMagnet(request.get_json() * 50)
    analyse.provideDataset(False, df)
    sig=[]
    app=[]
    same=[0]

    # Search from frequency range 1000000000 hertz to 900000000000 hertz
    for i in range(1000000000, 900000000000, 3000000000):
        signal = analyse.changeFrequency(i)
        #signal=signal if signal not in same else None
        if signal:
            print(len(signal[0]))
            # and (signal not in same)
            # same.append(signal)
            numericalAnalysis=CAN()
            signal=[numericalAnalysis.can(15, signal[1][1:].real), numericalAnalysis.can(15, signal[1][1:].imag)]
            fmt= "! 8s 8s"
            size = struct.calcsize(fmt)

            udp=UdPAnalyser()
            s=numericalAnalysis.qbits(signal[0])
            frame=udp.dump(s, fmt, size)
            if(frame not in sig):
                sig.append(frame)
                p=''.join(s)
                dumpShiftedLeft=[p] +[ ''.join([ hex(int(p[x:x+2], 16) ^ i)[2:] for x in range(int(len(p) / 2)) ]) for i in range(255) ]
                #print(p)
                print(dumpShiftedLeft)
                #os.system('./packetExtractor/script.sh {} > ./debug.json'.format(p))
                #if os.path.getsize("./debug.json"):
                #    with open('./debug.json', 'r') as debug:
                #        # if(debug.read() != "" and debug.read() != "[]"):
                #        app.append( json.loads(debug.read()) )
                #        print(json.dumps(app, indent=4))
                #dumpShiftedLeft=[ ''.join([ hex(int(p[x:x+2], 16) ^ i)[2:] for x in range(int(len(p) / 2)) ]) for i in range(255) ]
                for dt in dumpShiftedLeft:
                    os.system('./packetExtractor/script.sh {}'.format(dt))
                    if os.path.getsize("./debug.json"):
                        with open('./debug.json', 'r') as debug:
                            # if(debug.read() != "" and debug.read() != "[]"):
                            app.append( json.loads(debug.read()) )
                            print(json.dumps(app, indent=4))

    if len(app) > 0: 
        return json.dumps({ "frame": app })
    else:
        return json.dumps({ "state": "null" })

@app.route('/magnet', methods=['POST'])
def push():
    analyse = Analyse()
    udp=UdPAnalyser()
    analyse.provideDataset(os.getcwd() +'/radio.csv')
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