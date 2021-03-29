import socket
import matplotlib.pyplot as plt
import time
import struct

import numpy as np
from scipy import fftpack
import scipy.signal
from scipy import signal
import array
import resample as rs

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
def receive_data_UDP():
    # localhost
    UDP_IP = "127.0.0.1"

    # GQRX default port
    UDP_PORT = 7355

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    # initialize as a byte
    data = b'0'

    data_times = 1024

    f = open("radio-capture.dat", "rb")
    
    '''
    time_end = time.time() + 60*1
    while time.time() < time_end:
    #while data_times >= 0:
        data_temp, addr = sock.recvfrom(1024) # buffer size of 1024 bytes
        data = data + data_temp
        data_times -= 1
        #print("Received data: %s" % data)
    
    f.write(data)
    '''
    data = f.read()
    
    # generate t from 1 to len(data)
    t = list(range(len(data)))

    # Convert continuous stream of data into array of bytes
    data = bytearray(data)

    # Delete the last element to make data array have an even number of elements
    del data[len(data)-1:]
    # Do the same as above for t
    del t[len(t)-1:]


    #print(len(data))
    #print('='+str(len(data))+'h')

    # Turn array of bytes into an array of signed words
    data_16bit = array.array('h', data)
    # Because data comes in in reverse order, swap the bytes two by two for each word
    data_16bit.byteswap()
    
    #data_16bit = rs.resample(1800000, 20800, data_16bit)
    

    # Create a new t to match our array of words (shortened to half the size in bytes)
    t = list(range(len(data_16bit)))
    
    #no_samples = round(len(data) * float(4160) / 1800000) 
    #data_16bit = scipy.signal.resample(data_16bit, no_samples)
    #data_16bit = signal.resample(data_16bit, 28000)
    
    #f.write(data_16bit)
    f.close()

    #print(list(data_16bit))
    # plotting the data
    plt.figure(1)
    plt.plot(t,data_16bit) 
    
    #plt.show()
    
    #fig = plt.gcf()
    #fig.set_size_inches(15,10)
    #plt.savefig('input.png')

    # ###########################################
    # Below is code for testing only \/ \/
    # ###########################################

    def hilbert(data):
        analytic_signal = scipy.signal.hilbert(data)
        amplitude_envelope = np.abs(analytic_signal)
        return amplitude_envelope

    data_hilbert = hilbert(data_16bit)
    
    
    
    data_hilbert = rs.resample(48000, 4800, data_hilbert)
    #data_hilbert = signal.resample_poly(data_16bit, 1,10) # 10 looks decent
    
    
    

    plt.figure(2)
    #plt.plot(t,data_16bit,t[:len(data_hilbert)],data_hilbert) 
    plt.plot(t[:len(data_hilbert)],data_hilbert)
    
    #plt.show()
    #fig = plt.gcf()
    #fig.set_size_inches(15,10)
    #plt.savefig('demod.png')


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
    plt.figure(3)
    plt.plot(sample_freq, power)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('plower')
    
    plt.show()
    #fig = plt.gcf()
    #fig.set_size_inches(15,10)
    #plt.savefig('FFT.png')
    
    print("[receive_udp] Data saved to radio-capture.dat, input.png, demod.png, FFT.png")
    
    return data_16bit


