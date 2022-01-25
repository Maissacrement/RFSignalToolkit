import pandas as pd
import os
import json

dataset={'magnet': '[-35.88, -62.52, 77.04, -31.619999, -111.24, 105.78]', 'createdAtNs': '9768.961'}

def convertToMagnet(d):
    i=0
    d=list(d) * 3
    for r in range(0, int(len(d)/3)):
        m=dict(d[r*3])
        m['magnet']=json.loads(d[r*3]['magnet'])
        m['magnet']=[[m['magnet'][i], m['magnet'][i+2]] for i in range(int(len(m['magnet']) / 2)) ]
        m['time']=(float(m['createdAtNs']) - float(m['initialTime'])) / 1000000000
        d[r*3]=m
        tmp=d[r*3]['magnet']
        for coordinate in range(0, len(tmp)):
            append=dict(m)
            append['magnet']=tmp[coordinate]
            d[(r*3)+coordinate]=append
        
        i+=3

    return pd.DataFrame(d, index=['x', 'y', 'z']*(int((len(d)+1)/3)))

def convertToMagnetV1(d=dataset):
    magnet = list(json.loads(d['magnet']))
    d['magnet']=[[magnet[i], magnet[i+2]] for i in range(int(len(magnet) / 2)) ]
    d['time']= (int(d['createdAtNs']) - int(d['initialTime'])) / 1000000000
    return pd.DataFrame(data=d, index=['x', 'y', 'z'])

def magnet(d=dataset, filename='./magnet.csv', mode = 'w'):
    magnet = list(json.loads(d['magnet']))
    d['magnet']=[[magnet[i], magnet[i+2]] for i in range(int(len(magnet) / 2)) ]
    d['time']= (float(d['createdAtNs']) - float(d['initialTime'])) / 1000000000
    df = pd.DataFrame(data=d, index=['x', 'y', 'z'])
    if os.path.isfile(filename):
        mode = 'a'
    df.to_csv(filename, mode=mode, index=True, header=False if mode == 'a' else True)
    return { 'state': 'push' }