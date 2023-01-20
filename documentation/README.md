# Descrption of Our Goal

```bash
requirement: Fourrier Transform, Laplace Transfrom, biot & savart, magnetism.
 ```
In this project we are using a Smartphone Magnetic Sensor B(x, y, z) [Radio](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/radio.csv)


## Get signal indication (rssi, power, direction)

## Compute Magnitude of the magnetic field

$$
    B(t)=\sqrt{Bx(t)^2+By(t)^2+Bz(t)^2}
$$ 
 
With the help of above formula, you can find the magnitude of Magnetic field [[here]](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L91).


## Fourrier analysis


$$
    x(f) = \int_{-\infty }^{\infty}x(t)e^{-j2\pi ft}dt
$$


You can find the python function for fourier transform [here](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41)


## Demodulation

### ASK
Amplitude Shift Keying (ASK) is a type of digital modulation technique used to transmit data over a carrier wave. In ASK, the amplitude of the carrier wave is varied in order to represent the binary data. For example, a high amplitude could represent a digital 1, and a low amplitude could represent a digital 0.
ASK is a simple and easy-to-implement modulation technique, which makes it suitable for low-data-rate applications, such as remote control systems, garage door openers, and other similar devices that operate at low frequencies. However, due to its sensitivity to noise, it is generally not used in high-data-rate applications, such as wireless communications and satellite communications, where more robust modulation techniques such as Quadrature Amplitude Modulation (QAM) or Phase Shift Keying (PSK) are used. ASK is also used in RFID (Radio Frequency Identification) applications. RFID is a technology that uses radio waves to identify and track objects wirelessly. ASK is used in passive RFID systems, in which the reader sends a signal to the tag and the tag responds with its unique ID.

Digital signal can be modulated with the help ASK technique. The modulation scheme works based on the following formula:


$$
   s(t)= a*sin(2\pi f_{c}t);\ \ \ if bit = 1\\ 
$$

$$
    s(t) = 0 ;\ \ \ \ \ \ \ \ \ \ \ \ \ \ \  \ \ \ \ if bit = 0
$$

Amplitude Shift Keying (ASK) signal can be demodulated and digital data can be extracted from it based on the folling FSK demodulation scheme.

<img 
  src="../backend/asset/ask_demodulation.png"
  style="height:autopx;width:100%;"
/>

To implement ASK using Python, you can use the NumPy library to generate the carrier wave and the SciPy library to modulate the amplitude. First, you will need to create a carrier wave with a specific frequency and amplitude. Then, you can use a binary signal, such as a string of 0's and 1's, to modulate the amplitude of the carrier wave. For example, a 1 could represent a high amplitude and a 0 could represent a low amplitude. Finally, you can use the Matplotlib library to plot the modulated signal and observe the changes in amplitude.
Here is an example of how to implement ASK using Python:
```
import numpy as np
import matplotlib.pyplot as plt

# Generate the carrier wave
carrier_frequency = 10 # Hz
carrier_amplitude = 1 # arbitrary units
sampling_rate = 100 # samples per second
time = np.linspace(0, 1, sampling_rate)
carrier_wave = carrier_amplitude * np.cos(2 * np.pi * carrier_frequency * time)

# Modulate the carrier wave with a binary signal
binary_signal = [1, 0, 1, 0, 1, 1, 0, 0] # example signal
modulated_signal = np.zeros(len(binary_signal) * len(time))
for i, bit in enumerate(binary_signal):
    start = i * len(time)
    end = start + len(time)
    if bit == 1:
        modulated_signal[start:end] = carrier_wave
    else:
        modulated_signal[start:end] = -carrier_wave

# Plot the modulated signal
plt.plot(time,modulated_signal)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Modulated Signal')
plt.show()
```
This code generates a carrier wave with a frequency of 10 Hz and an amplitude of 1. Then, it modulates the amplitude of the carrier wave using a binary signal represented by an example array of [1,0,1,0,1,1,0,0]. This modulated signal is then plotted using the Matplotlib library.
It is important to notice that this is a very simple example of ASK with a low level of complexity and it would be useful only for educational purposes. In real-world applications, ASK is generally not used because it is highly sensitive to noise.


### FSK

In FSK, different carrier frequency waves are used to transmit digital 1 bit and digital 0 bit. Mathematically, it can be shown by the following equation:
 
$$
s(t) = a*sin(2\pi f_{c1}t);\ \ \ if bit = 1\\ 
$$

$$
s(t) = a*sin(2\pi f_{c2}t); \ \ \ if bit = 0
$$

Frequency Shift Keying (FSK) is a digital modulation technique that is used to transmit data over a carrier frequency by shifting the frequency of the carrier signal between two different frequencies. In FSK, the data signal is first converted into binary format, where a "1" is represented by one frequency and a "0" is represented by another frequency.

FSK is a form of frequency modulation, where the frequency of the carrier signal is changed according to the input data signal. The frequency of the carrier signal is shifted between two predetermined frequencies, known as the mark frequency and the space frequency. The mark frequency is used to represent a "1" in the data signal, while the space frequency is used to represent a "0".

FSK is widely used in wireless communication systems, such as in radio modems and in low-speed data communications. It is particularly useful in situations where the signal-to-noise ratio is low, as it is more resistant to noise and interference than other forms of modulation.

The main advantage of FSK over other forms of modulation is that it is relatively simple to implement and is relatively robust against noise and interference. It is also relatively easy to demodulate, as the receiver simply needs to detect which of the two frequencies is present in the received signal in order to recover the original data.

However, FSK also has some disadvantages. One of the main disadvantages is that it requires a relatively large bandwidth to transmit the data, as the mark and space frequencies are typically separated by several kilohertz. This can make it less suitable for use in situations where bandwidth is limited. Additionally, FSK is not as efficient as other forms of modulation, such as Phase Shift Keying (PSK), in terms of the amount of data that can be transmitted in a given amount of bandwidth.
Frequency Shift Keying (ASK) signal can be demodulated and digital data can be extracted from it based on the folling FSK demodulation scheme.

<img 
  src="../backend/asset/fsk_demodulation_1.png"
  style="height:autopx;width:100%;"
/>
In Python, FSK can be implemented using the numpy and scipy libraries to generate the carrier signal and modulate it with the data signal. The data signal is first converted into binary format, and then used to modulate the carrier signal by shifting its frequency between the two predetermined frequencies. The modulated signal can then be transmitted and demodulated on the receiving end to recover the original data signal.
Here is an example of how to implement FSK using Python:
```
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Define the carrier frequency, data signal, and frequency shift
carrier_frequency = 1000 # Hz
data_signal = [1, 0, 1, 0, 1, 1, 0, 0] # Binary data signal
frequency_shift = 100 # Hz

# Define the FSK modulation frequency
fsk_frequency = [carrier_frequency, carrier_frequency + frequency_shift]

# Generate the carrier signal
time = np.linspace(0, len(data_signal), num=len(data_signal)*1000)
carrier_signal = signal.square(2 * np.pi * carrier_frequency * time)

# Modulate the carrier signal with the data signal
modulated_signal = np.zeros(len(data_signal)*1000)
for i in range(len(data_signal)):
    modulated_signal[i*1000:(i+1)*1000] = signal.square(2 * np.pi * fsk_frequency[data_signal[i]] * time[i*1000:(i+1)*1000])
# Plot the modulated signal
plt.plot(time, modulated_signal)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Modulated Signal')
plt.show()
```
This code first imports the numpy, scipy and matplotlib libraries, then defines the carrier frequency, data signal, and frequency shift. The FSK modulation frequency is defined as the carrier frequency and the carrier frequency plus the frequency shift. The carrier signal is generated using the square wave function from the scipy library, with a frequency of the carrier frequency. Then, the carrier signal is modulated with the data signal by shifting its frequency between the two predetermined frequencies using a for loop. The modulated signal is then transmitted, and a demodulation process is applied on the received signal, to recover the original data signal. It compares the modulated signal with 0 if its greater than 0 it appends 1 otherwise 0 in the recovered_data list, which should match the original data signal.

Please keep in mind that this is a simple example, in real life applications it may require more complex demodulation process and error handling steps.



### PSK
Phase Shift Keying (PSK) is a digital modulation technique that uses the phase of a carrier wave to transmit information. In PSK, the phase of the carrier wave is shifted by a specific amount to represent different data symbols. This technique is widely used in communication systems such as wireless networks, satellite communications, and digital radios. PSK can be classified into two types: Binary Phase Shift Keying (BPSK) and Quadrature Phase Shift Keying (QPSK). BPSK uses two phase shifts, 0 and pi, to represent two data symbols 0 and 1, while QPSK uses four phase shifts, 0, pi/2, pi, and 3pi/2, to represent four data symbols. The main advantage of PSK is its high resistance to noise and interference, making it a reliable modulation technique in noisy environments. Additionally, PSK is relatively simple to implement and can be achieved with a low-cost circuit. However, it requires a relatively high signal-to-noise ratio to be transmitted effectively.
In PSK scheme, the phase of the carrier wave get shifted by pi for bit 1 and bit 0. Mathematically, it can be shows the following equation: 

$$
s(t) = a*sin(2\pi f_{c}t);\ \ \ if bit = 1\\ 
$$

$$
s(t) = a*sin(2\pi f_{c}t+\pi ); \ \ \ if bit = 0
$$

Phase Shift Keying (ASK) signal can be demodulated and digital data can be extracted from it based on the folling PSK demodulation scheme.

<img 
  src="../backend/asset/psk_demodulation.png"
  style="height:autopx;width:100%;"
/>
To implement PSK using Python, the first step is to generate a carrier wave. This can be done using the numpy library in Python, which provides functions for generating sine and cosine waves. Once the carrier wave is generated, the next step is to modulate the wave by shifting its phase. This can be done using the numpy.angle() function, which returns the phase of a complex number in radians. The phase shift can be set to a specific value, such as 0, pi/4, pi/2, etc., to represent different data symbols. Once the phase shift is applied, the modulated wave can then be transmitted or saved to a file for later use. To demodulate the signal, the phase shift can be determined using the numpy.angle() function and the data symbol can be reconstructed based on the phase shift. Overall, implementing PSK using Python is a relatively simple process that can be accomplished using basic mathematical functions and the numpy library.
Here is a sample code in Python that demonstrates how to generate a BPSK modulated signal:
```
import numpy as np
import matplotlib.pyplot as plt

# Define the carrier frequency and sampling rate
fc = 1000 # carrier frequency in Hz
fs = 10000 # sampling rate in Hz

# Generate the data symbols (0 or 1)
data = np.random.randint(0, 2, 1000)

# Generate the carrier wave
t = np.linspace(0, 1, fs)
carrier = np.cos(2*np.pi*fc*t)

# Modulate the carrier wave with the data symbols
modulated = np.zeros(len(data)*len(carrier))
for i in range(len(data)):
    if data[i] == 0:
        modulated[i*len(carrier):(i+1)*len(carrier)] = carrier
    else:
        modulated[i*len(carrier):(i+1)*len(carrier)] = -carrier

# Plot the modulated signal
plt.plot(modulated)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('BPSK Modulated Signal')
plt.show()

```
This code generates a BPSK modulated signal using a cosine carrier wave with a frequency of 1000 Hz and a sampling rate of 10000 Hz. The data symbols are randomly generated as 0 or 1. The carrier wave is modulated with the data symbols by shifting the phase by pi radians when the data symbol is 1. The resulting modulated signal is then plotted using the matplotlib library. Note that this code is just a simple example, in practice a more complex modulation scheme and error-correction should be used.


## Analog to digital converter (ADC, DAC)

Identify the peak from the signal: 1111 or F. The signal is quantized proportionally in frequency in numerical value.
I identify in my step value the one that repeats the most for one unit of the chosen sampling period.
The element repeated the most times in the sample becomes the maximum value of the right bit.
  Use them as a reference value to quantize the other signals (1111). F => F+F => 1111 1111

 
<img 
  src="../backend/asset/codage.png"
  style="height:autopx;width:100%;"
/>
 
Then I process the dump that I shift in time under .pcap with tshark in json

## HOW THIS WORK

1. First select [frequency](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L168).

2. From [Main](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L135) 

    2.1.  First we need to get the Magnetic Field Magnitude[(Normal)](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L91).

    2.2.  Second, transform signal into a  [complex](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L136) frequency form before computing the [fft](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41). 
    
    2.3. Get windowed data [cut](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41).

    2.4. Finally, Return the [filtered data](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/core/analyse.py#L41).

3. Init [CAN](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L170)
to Convert data from float into [hex dump](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L171). Then Convert hex dump into [ascii](https://github.com/Maissacrement/RFSignalToolkit/blob/main/backend/app.py#L175) data format.
