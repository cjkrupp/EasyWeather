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
'''
    # ###########################################
    # Below is code for testing only \/ \/
    # ###########################################
'''
def hilbert(data):
    analytic_signal = scipy.signal.hilbert(data)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma
    
def analysis(t,data_original,samplerate):
    
    print("analysis(): Starting analysis..")
    
    # Apply Butterworth filter with center Frequency 2400 Hz
    filter_config = scipy.signal.butter(2,2400,btype='lowpass',fs=samplerate,output='sos')
    data_original = signal.sosfilt(filter_config,np.asarray(data_original))
    
    # Apply Hilbert transform to demodulate signal
    data_hilbert = hilbert(data_original)
    
   

    '''
    ############################################
    # Plots
    ############################################
    '''
    #Un-Demodulated Raw Data
    plt.figure(1)
    plt.title("Original Signal")
    plt.plot(t,data_original) 
    plt.draw()  
    plt.show(block=False)
    
    #Demodulated (Hilbert)
    plt.figure(2)
    plt.title("Demodulated (Hilbert) Signal")
    plt.plot(t[:len(data_hilbert)],data_hilbert)
    plt.draw()  
    plt.show(block=False)

    # Plot the FFT
    time_step = 1/samplerate
    sig_fft = fftpack.fft(data_original)
    power = np.abs(sig_fft)**2
    sample_freq = fftpack.fftfreq(len(data_original), d=time_step)
    
    plt.figure(3)
    plt.title("FFT of Original Signal")
    plt.plot(sample_freq, power)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('plower')
    plt.draw()  
    plt.show(block=False)

    ######
    
    #data_hilbert_deriv = data_hilbert_deriv.values.tolist()
    
    #Derivative
    data_hilbert_deriv = pd.Series(data_hilbert).diff()
    peaks, _ = scipy.signal.find_peaks(data_hilbert_deriv, distance=2080,prominence=.2)
    plt.figure(4)
    plt.title("First Derivative of Demodulated Signal")
    #plt.plot(t[:len(data_hilbert_deriv)],data_hilbert_deriv,t[:len(data_hilbert_deriv)],data_hilbert_deriv[peaks], "x")
    plt.plot(data_hilbert_deriv)
    plt.plot(peaks,data_hilbert_deriv[peaks], "x")
    plt.show()
    
        '''
    inverse = np.subtract(np.amax(data_hilbert),data_hilbert)
    data_hilbert_deriv_corrected = np.multiply(inverse,data_hilbert)
    inverse = np.subtract(np.amax(data_hilbert_deriv_corrected),data_hilbert_deriv_corrected)
    data_hilbert_deriv_corrected = np.multiply(inverse,data_hilbert_deriv_corrected)
    inverse = np.subtract(np.amax(data_hilbert_deriv_corrected),data_hilbert_deriv_corrected)
    
    data_hilbert = pd.Series(inverse).diff()
    data_hilbert = data_hilbert.values.tolist()
 
    data_hilbert_deriv = inverse
    '''
 
    return data


