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

import platform
import receive_udp
import read_wav


import platform
import receive_udp
import analysis
import read_wav
import read_raw
import resample

# Hilbert() derived from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html
def hilbert(data):
    analytic_signal = scipy.signal.hilbert(data)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope


while 1:
    print("Starting EasyWeather..")

    # Read settings.csv to find what file receive_udp.py is writing to so that we can read it
    settings = open("settings.csv", "r")
    filename = settings.read()
    settings.close()
    print("Reading file: " + str(filename))
    
    # Read the current file over and over again in order to provide
    t,data_original,samplerate = read_raw.read_raw(str(filename))
    print("analysis(): Starting analysis..")
    
    
    new_sample_rate = 12000
    print(new_sample_rate)
    data_original = rs.resample(samplerate, new_sample_rate, data_original)
    samplerate = new_sample_rate
    t = list(range(len(data_original)))
    
    # Apply Butterworth filter with center Frequency 2400 Hz
    filter_config = scipy.signal.butter(1,2400,btype='lowpass',fs=samplerate,output='sos')
    data_original = signal.sosfilt(filter_config,np.asarray(data_original))

    filter_config = scipy.signal.butter(1,2400,btype='highpass',fs=samplerate,output='sos')
    data_original = signal.sosfilt(filter_config,np.asarray(data_original))
    
    # Apply Hilbert transform to demodulate signal
    data_hilbert = hilbert(data_original)

    #Derivative
    data_hilbert_deriv = pd.Series(data_hilbert).diff()
    peaks, _ = scipy.signal.find_peaks(data_hilbert_deriv, distance=int(math.floor(samplerate*.2)),prominence=.05)

    #Argentina
    #width = int(samplerate/2)+1#-10
        
    width = int(samplerate/4)

    new_peaks = []
    check_start = 0
    check_count = 0

    for i in range(len(peaks)-1):
        if ((peaks[i+1] - peaks[i]) > (width*.2)) and ((peaks[i+1] - peaks[i]) < (width*1.8)):
            check_start = i
            check_count = check_count + 1
        else:
            check_start = 0
            check_count = 0
        if check_count > 20:
            new_peaks.append(peaks[check_start])
            
    if (check_count > 20):
        print("Found image headers..")

    if len(new_peaks) == 0:
        new_peaks.append(0)


    plt.figure(1)
    
    data_hilbert_copy = data_hilbert[:math.floor(len(data_hilbert)/width)*width]
        
    data_hilbert_copy = np.roll(np.reshape(data_hilbert_copy,(-1,(width))), (0,-new_peaks[0]))

    reshaped = np.asarray(data_hilbert_copy)

    plt.cla()
    plt.imshow(reshaped,cmap='gray', vmin = np.mean(data_hilbert_copy)*.7, vmax = np.mean(data_hilbert_copy)*1.4)

    plt.draw()  
    #plt.show()
    plt.show(block=False)
    plt.pause(.05)
    input()
