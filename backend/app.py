#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import replace
from flask_cors import CORS,cross_origin
from flask import Flask, Response, request, render_template, send_from_directory
from flask.helpers import safe_join
from nbformat import write
import requests

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
from dotenv import load_dotenv
from core.Translator.DeeplAPI import Deepl
from deep_translator import GoogleTranslator
import gettext
import hexdump
import re

# Load dotenv
load_dotenv()
TRACKER_URL=os.getenv('TRACKER_URL')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')

# SIGNAL FREQUENCY TYPE
signalRange={
  #'bluetooth': [.00001, .00002, .0001, 2400, 2483.5, 60000, 200000, 600000],
  #'wimax': [10000, 66000, 2000, 11000],
  #'lorawan': [433.05, 434.79, 863, 870, 902.3, 914.9],
  #'wifi': [2.4 * (10**3), 5 * (10**3), 60 * (10**3)],
  #'other': [9.20  * (10**3)],
  #'manet': [433  * (10**3)],
  #'MICS_Band': [402 * (100**6), 405 * (100**6)],
  #'HBC_Band': [5 * (100**6), 50 * (100**6)],
  #'WMTS_Band': [863 * (100**6), 870 * (100**6)],
  #'Narrowband': [2360 * (100**6), 2400 * (100**6)],
  #'World_Wide': [2400 * (100**6), 2450 * (100**6)],
  #'UWB_Band': [3100 * (100**6), 10600 * (100**6)],
  'nrf': [2476]


}

wireless=[]
[ wireless.extend(x) for x in map(lambda x: signalRange.get(x), signalRange.keys()) ]

def extractor(dumplist):
    dumplist=[ *filter(lambda x: len(x.strip()) != 0, dumplist) ]
    MTU=1125# 1125 octet --> 9000 byte Jumbo ?
    count=int(len(dumplist)//MTU)
    count=count if count != 0 else 1
    print('searching..')
    try:
        text=''
        for i in range(int(len(dumplist) / count)):
            dump="".join(dumplist[i*count:(1+i)*count])
            sentence=''.join([ bytes.fromhex(dump[x:x+4]).decode('utf-16', 'replace').encode('utf-8').decode('utf-16', 'replace') for x in range(int(len(dump) / 4)) ])
            text+='\n' + sentence
            
        with open('./packetExtractor/set', 'ab+') as res:
            res.write(bytes('{}\n*\n'.format(text).encode('utf-8')))
        res.close()
        cutw=1000
        regex0=r'[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\'\.\,]'
        text=' '.join([*filter(lambda x: x, re.split(regex0, text)) ])
        tmp=''
        for i in range(int(len(text) / cutw)):
            sentence=gettext.gettext(text[i*cutw:(i+1)*cutw:1])
            try:
                sentence = GoogleTranslator(source='auto', target='fr').translate(sentence)
            except:
                sliceto=int(len(sentence)//8)
                for j in range(sliceto):
                    sentence = GoogleTranslator(source='auto', target='fr').translate(sentence[j*sliceto:(j+1)*sliceto])
            sentence=Deepl().translate(str(sentence))
            regex0=r'[^a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ@_\'\.\,\<\>]'
            tmp=' '.join([*filter(lambda x: x, re.split(regex0, sentence)) ])
            sentence=hexdump.hexdump(tmp.encode('utf-8'), result='return')
            print(tmp)
                
    finally:
        print("End")

def iptrack():
    data=""
    try:
        data=subprocess.run(["{}/packetExtractor/ips.sh".format(os.getcwd()), "{}/packetExtractor/set".format(os.getcwd())], stdout=subprocess.PIPE)
        if data.returncode == 0:
            for ip in [*filter(lambda x: len(x)>0, data.stdout.decode("utf-8").split('\n'))]:
                response=requests.get(TRACKER_URL + '/list/{}'.format(ip))
                yield bytes(response.text.encode('utf-8'))
    finally:
        print("End")        

app = Flask(__name__)
static = safe_join(os.path.dirname(__file__), 'views')
CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,origin,*"
cors = CORS(
    app, origins=CORS_ALLOW_ORIGIN.split(","), 
    allow_headers=CORS_ALLOW_HEADERS.split(","),
    expose_headers= CORS_EXPOSE_HEADERS.split(","),
    resources={r"/*": {"origins": "*"}},
    supports_credentials = True
)

@app.route('/data', methods=['GET'])
@cross_origin(supports_credentials=True)
def views():
    return send_from_directory(static, 'index.html')
    
@app.route('/data/text', methods=['GET'])
def translatedtext():
    return """<h1>Hello, World!</h1>"""

@app.route('/data/json', methods=['GET'])
@cross_origin(supports_credentials=True)
def jsondata():
    return Response(iptrack(), mimetype="application/json", headers={
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Authorization, Accept',
    })

@app.route('/dynmagnet', methods=['POST', 'GET'])
def dyns():
    analyse = Analyse()
    signal = None
    dumpShiftedLeft=[]
    i = 2400
    df=convertToMagnet(request.get_json())
    sig=[]

    # Search from frequency range 1000000000 hertz to 900000000000 hertz
    for FREQUENCY in wireless:
        print('[APP]: is running for {} Mhz'.format(FREQUENCY))
        analyse.provideDataset(False, df)
        signal = analyse.changeFrequency( FREQUENCY )
        signal[1].tofile('data2.csv', sep = ',')
        if signal:
            numericalAnalysis=CAN()
            s=numericalAnalysis.qbits(numericalAnalysis.can(15, signal[1].real))
            if(s not in sig):
                p=''.join(s)
                sig.append(p)
                dumpShiftedLeft+=[p] +[ ''.join([ hex(int(p[x:x+2], 16) ^ i)[2:] for x in range(int(len(p) / 2)) ]) for i in range(127) ]

    return Response(extractor(dumpShiftedLeft), mimetype="application/json")

@app.route('/magnet', methods=['POST'])
def push():
    return json.dumps({
        'magnet': [magnet(req, mode = 'w' if i == 0 else 'a', filename='./radio.csv') for i, req in enumerate(request.get_json())],
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host=HOST, port=PORT)