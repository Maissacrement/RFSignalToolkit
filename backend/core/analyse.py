from math import nan
from scipy.fftpack import fftfreq
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt


"""
    Analyse() is python Class used magnet field area to
    transform it into oem signal wave. OEM contains area
    network wifi, bleutooth, gsm, 4g, 3gpp, rf, other 
    communication device.
"""
class Analyse:
    def __init__(self):
        self.signal = []
        self.secondLength = 0
        self.start_time = 0
        self.dataset = None

        self.filteredFreq=(lambda omega, omegaFrequency, target=15000, window=2000: 
            [ [omega[i], freq] for i, freq in enumerate(omegaFrequency) if self.isInInterval(freq, target, window) ]
        )

    
    """
        Window a value from Array
    """
    def isInInterval(self, x, interval=15000, w=1000):
        s = [interval-w, interval+w]
        u = (x > s[0] and x < s[1]) if x > 0 else (x < s[0] and x > s[1])
        return True if u else False

    """
        Transformer de fourier
        Pour t fixer avec X=j2pift et A=amplitude(B) et B la norme du champ magnetique
        on a f(t) = x(t) * (cos(X) - sin(X))
    """
    def f(self, A, t, Te, w=2*np.pi):
        return A * ( np.cos( w*t/Te ) - np.sin( w*t/Te ) ) # f(t) = A * e

    """
        Signal recu
        signal: Tableau de format f(t) = x(t) * (e**j2pift)
        frequency: Tableau de frequence du signal recu
        pure: signal without fourier 
    """
    def getSignalFrom(self, A, fe=50000):
        signal, p=[], 0
        for i in range(self.secondLength):
            omegaN=len(self.getSetBySecond(i+1))
            if(i!=0):
                [ signal.append(self.f(a, i, omegaN)) for a in A[p:p+omegaN]]
                p+=omegaN

        return {
            "signal": np.fft.fft(np.abs(signal)) if len(signal) else None,
            "frequency": fftfreq(len(signal), d=1/fe) if len(signal) else None,
            "pure": np.abs(signal)
        }

    """
        Filter Frequency make window
        omega: Tableau de format f(t) = x(t) * (e**j2pift)
        omegaFrenquency: Representation frequentiel d'Omega
        target: Frequence cible
        window: Fenetre d'exploitation
    """
    def signalToDict(self, signal):
        x = {'signal': [], 'frequency': []}
        for el in signal:
            x['signal'].append(el[0])
            x['frequency'].append(el[1])

        x['pure']=np.abs(x['signal'])
        x['signal']=np.fft.fft(np.abs(x['signal']))
        return x 

    
    """
        Get Dataframe Magnet Value at specified second
        second: number (time first to fetch dataframe value)
    """
    def getSetBySecond(self, second):
        return self.dataset[(self.dataset["time"] > self.start_time + second) & (self.dataset["time"] < self.start_time + second + 1)]
    
    """
        Champ magnetic normalisé
    """
    def getMagneticFieldNormal(self):
        magnet = [ x if type(x) == list else json.loads(x) for x in self.dataset['magnet'].values  ]

        self.start_time=int(self.dataset["time"][1])
        end_time=int(self.dataset["time"][-1])
        self.secondLength = end_time - self.start_time
        
        return [ np.absolute(magnet[(x*3)][0] + magnet[(x*3)][0] + magnet[(x*3)][0]) * (10**-9) for x in range(int(len(magnet)/3))]


    """
        Plot signal
    """
    def plotSignal(self, freq, signal, f=75000, w=6000):
        plt.xlabel(r"Frequence (Hz)")
        plt.ylabel(r"Amplitude $X(f)$")
        plt.plot(freq, signal, label="Signal")
        plt.xlim(f-w,f+w)
        plt.show()

    """
        Provide dataset Array<Magnet> or CSV
        name: if csv csv name
        B: if magnet Array value Array<Magnet>
    """
    def provideDataset(self, name=False, B=None):
        if name: 
            self.dataset = pd.read_csv(name, index_col=0)
        else:
            self.dataset = B
        

    """
        Change Radio Fm station
        Fm station in hertz
    """
    def changeFrequency(self, Fm=60): # 5.0 mhz
        pound={ "khz": (10**3), "mhz": (10**6), "ghz": (10**9) }
        Fm=Fm*pound['mhz']
        B=self.getMagneticFieldNormal()
        sig=self.getSignalFrom(B, Fm)
        if type(sig["signal"]) != type(None):
            signal=sig.get('signal')
            freq=sig.get('frequency')
            Fe=(Fm / 2)
            scope=Fe / 20
            sig=self.filteredFreq(signal, freq, Fe, scope) + self.filteredFreq(signal, freq, Fe*2, scope)
            if sig: 
                sig=self.signalToDict( sig )
                signal=sig.get('signal')
                freq=sig.get('frequency')

                return [ freq, signal ]
        return None


"""
# Remove comment at top and bottom if you want try.
# 

# Define dataset
df=[{"magnet": "[-35.88, -62.52, 77.04, -31.619999, -111.24, 105.78]", "createdAtNs": "8274324561851", "initialTime": "10811745345305"}] # magnet data

# Instanciated CLass
analyse=Analyse()

# Provide dataset
analyse.provideDataset(False, df) # First arg is csv name location, seconde arg is Array of Object

# Get Signal at Specified frequencies in Mhz
print(analyse.changeFrequency(60000)) # 60 Ghz
"""
