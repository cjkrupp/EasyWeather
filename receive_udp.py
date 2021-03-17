import socket
import matplotlib.pyplot as plt
import time
import struct

import numpy as np
from scipy import fftpack
import scipy.signal
import array

'''
    https://gqrx.dk/doc/streaming-audio-over-udp
    
    GQRX Import format
    Channels: 1 (left)
    Sample rate: 48 kHz
    Sample format: 16 bit signed, little endian (S16LE)
    
    
    
    NOAA 15 - 137.6200 MHz
    NOAA 18 - 137.9125 MHz
    NOAA 19 - 137.1000 MHz

'''

# localhost
UDP_IP = "127.0.0.1"

# GQRX default port
UDP_PORT = 7355

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# initialize as a byte
data = b'0'

data_times = 1024

f = open("radio-capture.dat", "ab")
#time_end = time.time() + 60 #60*15
#while time.time() < time_end:
while data_times >= 0:
    data_temp, addr = sock.recvfrom(1024) # buffer size of 1024 bytes
    data = data + data_temp
    data_times -= 1
    #print("Received data: %s" % data)

# generate t from 1 to len(data)
t = list(range(len(data)))

# Convert continuous stream of data into array of bytes
data = bytearray(data)

# Delete the last element to make data array have an even number of elements
del data[len(data)-1:]
# Do the same as above for t
del t[len(t)-1:]


print(len(data))
print('='+str(len(data))+'h')

# Turn array of bytes into an array of signed words
data_16bit = array.array('h', data)
# Because data comes in in reverse order, swap the bytes two by two for each word
data_16bit.byteswap()

# Create a new t to match our array of words (shortened to half the size in bytes)
t = list(range(len(data_16bit)))

#f.write(data_16bit)
f.close()

print(list(data_16bit))
# plotting the data
plt.plot(t,data_16bit) 
plt.show()


# ###########################################
# Below is code for testing only \/ \/
# ###########################################

def hilbert(data):
    analytic_signal = scipy.signal.hilbert(data)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope

data_hilbert = hilbert(data_16bit)

plt.plot(t,data_16bit,t,data_hilbert) 
plt.show()



time_step = 1/48000

#total_data = (np.sin(2 * np.pi*1600*time_vec))
# The FFT of the signal
sig_fft = fftpack.fft(data_16bit)

# And the power (sig_fft is of complex dtype)
power = np.abs(sig_fft)**2
# The corresponding frequencies
sample_freq = fftpack.fftfreq(len(data_16bit), d=time_step)

# Plot the FFT power
#plt.figure(figsize=(6, 5))
plt.plot(sample_freq, power)
plt.xlabel('Frequency [Hz]')
plt.ylabel('plower')
plt.show()





