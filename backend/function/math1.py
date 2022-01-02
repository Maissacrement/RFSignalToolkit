import numpy as np

def isInInterval(x, interval=15000, w=1000):
    s = [interval-w, interval+w]
    u = (x > s[0] and x < s[1]) if x > 0 else (x < s[0] and x > s[1])
    return True if u else False

filtered_freq=(lambda omega, omegaFrequency, target=15000, window=2000: 
    [ [omega[i], freq] for i, freq in enumerate(omegaFrequency) if isInInterval(freq, target, window) ]
)

# FREQUENCE
instanceSineWave = lambda omega_e, fe, f: [np.sin(2 * np.pi * f * x/fe) for x in omega_e]

# Electromagnetism

# Constante
Q=1.6 * (10**-19) # Coulomb
mu0=4 * np.pi * (10**7) #  kg m A−2 s−2
C=6.241 * (10**18) # A.s-1

# B normeDuChampsMagnetique V normeDeLavitesse
Foem=lambda V, B: Q * ( V * B )
