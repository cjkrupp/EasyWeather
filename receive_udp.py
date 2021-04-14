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
import math
import pandas as pd
from scipy.io import wavfile
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

    #f = open("radio-capture.dat", "rb")
    samplerate, data = wavfile.read('argentina.wav')
    '''
    time_end = time.time() + 60*2.9
    while time.time() < time_end:
    #while data_times >= 0:
        data_temp, addr = sock.recvfrom(1024) # buffer size of 1024 bytes
        data = data + data_temp
        data_times -= 1
        #print("Received data: %s" % data)
    
    f.write(data)
    '''
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
    '''
    data_16bit = data #[:,1]
    print(data)
    
    #data_16bit = rs.resample(1800000, 20800, data_16bit)
    

    # Create a new t to match our array of words (shortened to half the size in bytes)
    t = list(range(len(data_16bit)))
    
    #no_samples = round(len(data) * float(4160) / 1800000) 
    #data_16bit = scipy.signal.resample(data_16bit, no_samples)
    #data_16bit = signal.resample(data_16bit, 28000)
    
    #f.write(data_16bit)
    #f.close()

    #print(list(data_16bit))
    
    
    #Un-Demodulated raw data
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
    
    def movingaverage (values, window):
        weights = np.repeat(1.0, window)/window
        sma = np.convolve(values, weights, 'valid')
        return sma
    
    #filter_config = scipy.signal.butter(2,1200,btype='lowpass',fs=48000,output='sos')
    #data_16bit = signal.sosfilt(filter_config,np.asarray(data_16bit))
    
    #b, a = signal.iirnotch(2400, 10, 48000)
    #freq, h = signal.freqz(b, a, fs=48000)
    #data_16bit = np.convolve(data_16bit,h,'same').real
    
    filter_config = scipy.signal.butter(2,2400,btype='lowpass',fs=samplerate,output='sos')
    data_16bit = signal.sosfilt(filter_config,np.asarray(data_16bit))
    
    
    
    
    #data_hilbert = data_16bit
    data_hilbert = hilbert(data_16bit)
    
    #data_16bit = rs.resample(48000, 4800, data_16bit) #best so far 48000,4800
    
    
    
    #data_hilbert = movingaverage(data_hilbert,20)
    
    #filter_config = scipy.signal.butter(2,4800/4,fs=4800,output='sos')
    #data_hilbert = signal.sosfilt(filter_config,np.asarray(data_hilbert))
    
    '''
    # select a limited amount of data (585000 elements)
    print(len(data_16bit[:585284]))
    data_16bit = data_16bit[:585000]
    
    # how much to shift the image by (x and y)
    i = 2334
    k = 2080
    while 1:
        
        #          turn a 1d array of data into a 2d array
        #           |               circular rotate the array
        #           \/              \/                      round down
        data_tmp = (np.reshape( np.roll(   data_16bit[:math.floor(585000/int(650+0))*int(650+0)],    (0,i) ),   (int(650+0),-1))   )
        
        
        reshaped = np.asarray(data_tmp)
        plt.figure(1)
        plt.cla()
        plt.imshow(reshaped,cmap='gray', vmin = -200, vmax = 4000)
        print("shape: "+str(k)+' '+str(i))
        plt.draw()  
        plt.show(block=False)
        
        # increment for searching the image for the actual image rotation
        i = i + 100
        k = k+1
        
        # pause
        input()
    
    '''
    
    #Demodulated (Hilbert)
    plt.figure(2)
    #plt.plot(t,data_16bit,t[:len(data_hilbert)],data_hilbert) 
    #plt.plot(t[:len(data_hilbert)],data_hilbert)
    plt.plot(t[:len(data_hilbert)],data_hilbert)
    plt.draw()  
    plt.show(block=False)
    #plt.show()
    #fig = plt.gcf()
    #fig.set_size_inches(15,10)
    #plt.savefig('demod.png')


    time_step = 1/samplerate#1/48000

    #total_data = (np.sin(2 * np.pi*1600*time_vec))
    # The FFT of the signal
    sig_fft = fftpack.fft(data_16bit)

    # And the power (sig_fft is of complex dtype)
    power = np.abs(sig_fft)**2
    # The corresponding frequencies
    sample_freq = fftpack.fftfreq(len(data_16bit), d=time_step)


    # Plot the FFT power
    plt.figure(3)
    plt.plot(sample_freq, power)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('plower')
    plt.draw()  
    plt.show(block=False)
    #plt.show()
    #fig = plt.gcf()
    #fig.set_size_inches(15,10)
    #plt.savefig('FFT.png')
    
    print("[receive_udp] Data saved to radio-capture.dat, input.png, demod.png, FFT.png")
    
    #Derivative
    data_hilbert = pd.Series(data_hilbert).diff()
    data_hilbert = data_hilbert.values.tolist()
    plt.figure(4)
    plt.plot(t[:len(data_hilbert)],data_hilbert)
    plt.show()
    
    return data_16bit


