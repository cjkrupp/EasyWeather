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

# Returns array of 16 bit values from UDP server
#data = receive_udp.receive_data_UDP()
#t,data,samplerate = read_wav.read_wav('argentina.wav')
 


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
# Hilbert() derived from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html
def hilbert(data):
    analytic_signal = scipy.signal.hilbert(data)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope


def analysis(t,data_original,samplerate):
    
    print("analysis(): Starting analysis..")
    t_orig = list(range(len(data_original)))
    
    new_sample_rate = 12000
    
    if (samplerate > new_sample_rate):
        print("Resampled to " + str(new_sample_rate) + " Hz")
        data_resample = rs.resample(samplerate, new_sample_rate, data_original)
        samplerate = new_sample_rate
        
        # Apply Butterworth filter with center Frequency 2400 Hz
        filter_config = scipy.signal.butter(1,2400,btype='lowpass',fs=samplerate,output='sos')
        data_resample = signal.sosfilt(filter_config,np.asarray(data_resample))

        filter_config = scipy.signal.butter(1,2400,btype='highpass',fs=samplerate,output='sos')
        data_resample = signal.sosfilt(filter_config,np.asarray(data_resample))
    else:
        data_resample = data_original
    
    t = list(range(len(data_resample)))
    # Apply Hilbert transform to demodulate signal
    data_hilbert = hilbert(data_resample)

    #Derivative
    data_hilbert_deriv = pd.Series(data_hilbert).diff()
    peaks, _ = scipy.signal.find_peaks(data_hilbert_deriv, distance=int(math.floor(samplerate*.2)),prominence=.05)

    if (samplerate == 11025):
        width = int(samplerate/2)+1
    else:
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


    plt.figure()
    
    data_hilbert_copy = data_hilbert[:math.floor(len(data_hilbert)/width)*width]
        
    data_hilbert_copy = np.roll(np.reshape(data_hilbert_copy,(-1,(width))), (0,-new_peaks[0]))

    reshaped = np.asarray(data_hilbert_copy)

    plt.cla()
    plt.imshow(reshaped,cmap='gray', vmin = np.mean(data_hilbert_copy)*.7, vmax = np.mean(data_hilbert_copy)*1.4)

    plt.draw()  
    #plt.show()
    plt.show(block=False)
    plt.pause(.05)
    detailed_graphs = input("Enter 1 for detailed analysis graphs, otherwise press any key to quit:")
    
    if (detailed_graphs == '1'):


        ############################################
        # Analysis Plots
        ############################################
    
        #Un-Demodulated Raw Data
        plt.figure()
        plt.title("Original Signal")
        plt.plot(t_orig,data_original) 
        plt.draw()  
        plt.show(block=False)
        
        #Demodulated (Hilbert)
        plt.figure()
        plt.title("Demodulated (Hilbert) Signal")
        plt.plot(t[:len(data_hilbert)],data_hilbert)
        plt.draw()  
        plt.show(block=False)

        # Plot the FFT
        time_step = 1/samplerate
        sig_fft = fftpack.fft(data_original)
        power = np.abs(sig_fft)**2
        sample_freq = fftpack.fftfreq(len(data_original), d=time_step)
        
        plt.figure()
        plt.title("FFT of Original Signal")
        plt.plot(sample_freq, power)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('plower')
        plt.draw()  
        plt.show(block=False)

        
        #Derivative
        data_hilbert_deriv = pd.Series(data_hilbert).diff()
        peaks, _ = scipy.signal.find_peaks(data_hilbert_deriv, distance=int(math.floor(samplerate*.2)),prominence=.05)
        
        new_peaks = []
        check_start = 0
        check_count = 0
        sample_width = int(math.floor(samplerate*.5))
        for i in range(len(peaks)-1):
            if ((peaks[i+1] - peaks[i]) > (sample_width*.2)) and ((peaks[i+1] - peaks[i]) < (sample_width*1.8)):
                check_start = i
                check_count = check_count + 1
            else:
                check_start = 0
                check_count = 0
            if check_count > 10:
                new_peaks.append(peaks[check_start])
            
        
        if len(new_peaks) == 0:
            new_peaks.append(0)
        
        plt.figure()
        plt.title("First Derivative of Demodulated Signal")
        plt.plot(data_hilbert_deriv)
        plt.plot(peaks,data_hilbert_deriv[peaks], "x")
        plt.draw()  
        plt.show(block=False)
        
        plt.figure()
        plt.title("Orig Signal With Peak Detection")
        plt.plot(data_hilbert)
        plt.plot(new_peaks,data_hilbert[new_peaks], "bo")
        plt.draw()  
        plt.show()
        
    else:
        return 0
        
  
        
        




