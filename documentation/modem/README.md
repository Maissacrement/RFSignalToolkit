# Chirp Modulation & Demodulation
## Introduction
Chirp in tandem with spectrum spreading yields a
modulation scheme with its on special characteristics, in which the scheme is called Chirp Spread Spectrum (CSS). The what, why and how to take advantage of CSS followed by its demodulation mechanisms are addressed beriefly here. More detail can be found in the modem working dir

## The what
Chirp is a signal whose frequency changes over time. In the general complex plane, chirp can be provided as:
$$
    x(t) = Ae^{j\theta (t)}
$$
Hence, the **instantaneous frequency** of chirp signal at time $t$ becomes:
$$
    f(t) = \frac{1}{2\pi}\frac{d\theta(t)}{dt}
$$

## The why
From the angle of this project, one motive for integrating chirp signaling based modulation into the radio interface layer of the system could be its potential for real-time sensing and localization of communication nodes. It could be idela for low power & long range operation

## The how

A simple digital modulation scheme can be constructed by mapping binary input data into up-chirp
and down-chirp, just like FSK modulation. But as noted, spectrum spreading based chirp signaling provides more positive features, and hence CSS modulation that goes more like SPREADING + CHIRPING