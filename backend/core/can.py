from math import *
import numpy as np

class CAN:
    def __init__(self):
        self.signal = []

    """
        Arrondi 
    """
    def r0(self, number):
        return ceil(number) if number > int(number) + .75 and int(number) < 15 else floor(number)

    """
        Convertisseur analogique to numerique (Y)
    """
    def can(self, nbit=16, In=[8.5,9,50,7,9]):
        nbit = (nbit / max(In)) if max(In) > np.abs(min(In)) else (nbit / -max(In))
        return [ self.r0(np.abs(In[n] * nbit))  for n in range(len(In)) ]

    """
        Convert number to hex
    """
    def unpackNBytesArray(self, data, N=16):
        filter=['a','b','c','d', 'e', 'f']
        return [ map(lambda x: str(np.abs(x)) if np.abs(x) < 10 else filter[10-np.abs(x)], data[N*i:N*(i+1)]) for i in range(int( len(data) / N) - 1 ) ]

    """
        Quantified X as occured value reduncy
        data: Array of numerical value from CAN
    """
    def unpackQBitArray(self, data, N=15):
        tmp=[]
        data=[ x for x in data]
        uniq=[ [data.count(x), x] for x in set(data)]
        k=[data.count(x) for x in set(data)]
        nbit = float(N / max(k))

        for i in range(len(data)):
            id=[ *filter(lambda x: data[i] == x[1], uniq) ][0][0]
            Quantum=int(self.r0(int(id * nbit)))
            Quantum=hex(Quantum)[2:] if Quantum > 9 else Quantum
            tmp.append( str(Quantum) + str(data[i]) )

        return tmp

    """
        Formated hex output of dump rf
    """
    def qbits(self, signal):
        s=[ hex(np.abs(s))[2:] for s in signal]
        s=np.concatenate([ list(data) for data in s ]).tolist()
        
        return self.unpackQBitArray(s, N=15)

# can=CAN()
# can.r0(5.8)
# Only for % 16 bits > array (32, 64, ...)
# can.unpackNBytesArray([10, 15, 13, 1,1,1,1,1,1,1,1,4,5,5,12,1,1,1,4,5])
# can.unpackQBitArray([10, 15, 13, 1,1,1,1,1,1,1,1,4,5,5,12,1,1,1,4,5])
