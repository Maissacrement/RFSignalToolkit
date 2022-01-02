#!/usr/bin/env python3
from core.analyse import Analyse
from core.can import CAN
from core.udpAnalyser import UdPAnalyser
from flask import Flask, Response, request
import matplotlib.pyplot as plt
from function.math1 import instanceSineWave
from function.dataframes import magnet, convertToMagnet
import struct
import json
from flask_cors import CORS,cross_origin
import os
import numpy as np
import function.packetReader as packet


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/dynmagnet', methods=['POST', 'GET'])
def dyns():
    import pandas as pd

    df = pd.DataFrame({})
    analyse = Analyse()
    signal = None
    i = 1

    df=convertToMagnet(request.get_json())
    analyse.provideDataset(False, df)
    sig=[]

    for i in range(700, 720):
        signal = analyse.changeFrequency(i)
        if signal:
            numericalAnalysis=CAN()
            signal=[numericalAnalysis.can(15, signal[1].real), numericalAnalysis.can(15, signal[1].imag)]
            fmt= "! 8s 8s"
            size = struct.calcsize(fmt)

            udp=UdPAnalyser()
            print(signal[0])
            s=numericalAnalysis.qbits(signal[0])
            frame=udp.dump(s, fmt, size)
            if(frame): print(str(i), " MHZ")
            sig.append({ "state": "found", "frame": frame, "frequency": str(i) + " GHZ" })
            
            print(s)
            #packet.hexToUri(s)

        else: 
            return json.dumps(sig)

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