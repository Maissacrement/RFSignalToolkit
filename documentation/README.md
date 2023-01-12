# Descrption of Our Goal

```bash
requirement: Fourrier, Laplace, biot & savart, magnetism.
 ```

Using is smartphone magnet sensor B(x, y, z) [Radio](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/radio.csv)


## Get signal indication (rssi, power, direction)

## Compute magnetique field

$$
    B(t)=\sqrt{Bx(t)^2+By(t)^2+Bz(t)^2}
$$ 
 
Here u can found the [Normal](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L91). This normal is used as amplitude.


## Fourrier analysis

$$
    X(f)=B*e^{-j*t*f*pi}
    
$$

Here u can found fourrier analysis [here](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41)


## Demodulation

### ASK

...

### FSK

...

### PSK

...

## Analog to digital converter (ADC, DAC)

Identify peak from time signal. Signal is quantified in my CAN proportionnally at amplitude peak (1111) F

After that i identify in my step value the one that is repeated the most. Using them as refered value to quantify the other (1111). F => F+F => 1111 1111
 
<img 
  src="../backend/asset/codage.png"
  style="height:100px;width:auto;"
/>
 
Knowing that the signal obtained is represented in this way
 
(Time can, Intensity can)
(1111 1111) ---> 0F

Knowing that the signal obtained is represented by this We have therefore recovered a data element
To do the time can we refer to the number of times that an intensity value is repeated, i.e. the number of frequency periods. We then have:
 
(1111 1111) --> FF
This is the first period treated
So we have our first one element of our dump
The strongest intensity value is therefore the reference for proportionally deducing the other values
Then I process the dump that I shift over time under .pcap with tshark in json

## HOW THIS WORK

First select [frequency](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L168).

From [Main](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L135) we need to get [Magnetic field Normal](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L91). In second time, transform signal into a  [complex](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L136) from frequency before a [fft](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41). Get windowed data [cut](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41).
Return [filtered data](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41).

Init [CAN](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L170)
Convert data float into [hex dump](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L171). Convert hex dump in [ascii](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L175)