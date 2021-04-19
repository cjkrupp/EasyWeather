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

'''
This file is where execution always starts. It will determine where to get
data from and what OS is running.

'''


platform_linux = 1
running_platform = 0

'''
if (platform.system() == "Linux"):
    running_platform = 1
    print("It looks like you are running Linux, starting rtl_sdr capture.")
'''
def hilbert(data):
    analytic_signal = scipy.signal.hilbert(data)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

if 1==1:
#while 1:
    #val = input("Enter which satellite to capture: ") 
    print("Starting EasyWeather..")
    #t,data,samplerate = receive_udp.receive_data_UDP(60*5,'test')
    #t,data,samplerate = read_wav.read_wav('argentina.wav')
    #t,data,samplerate = read_wav.read_wav('19mar21.wav')
    t,data_original,samplerate = read_raw.read_raw('radio_capture4.dat')
    #t,data,samplerate = read_raw.read_raw('radio-capture.dat')
    #samplerate = 1800000
    #analysis.analysis(t,data,samplerate)
    #data_original = resample.resample(samplerate,18000,data_original)
    #samplerate = 18000
    #print(type(data_original[0]))
    #input()
    #data_original = scipy.signal.resample(data_original,int(len(data_original)/10))





        
    print("analysis(): Starting analysis..")

    #data_original = rs.resample(48000, 4800, data_original)
    #t = list(range(len(data_original)))

    # Apply Butterworth filter with center Frequency 2400 Hz
    filter_config = scipy.signal.butter(1,2400,btype='lowpass',fs=samplerate,output='sos')
    data_original = signal.sosfilt(filter_config,np.asarray(data_original))

    filter_config = scipy.signal.butter(1,2400,btype='highpass',fs=samplerate,output='sos')
    data_original = signal.sosfilt(filter_config,np.asarray(data_original))


    # Apply Hilbert transform to demodulate signal
    data_hilbert = hilbert(data_original)



    #data_hilbert_deriv = data_hilbert_deriv.values.tolist()

    #Derivative
    data_hilbert_deriv = pd.Series(data_hilbert).diff()
    peaks, _ = scipy.signal.find_peaks(data_hilbert_deriv, distance=int(math.floor(samplerate*.1)),prominence=.05)
    #peaks, _ = scipy.signal.find_peaks(data_hilbert_deriv, distance=100,prominence=.9)

    new_peaks = []
    check_start = 0
    check_count = 0
    sample_width = 4000 #int(math.floor(samplerate/11.9))
    for i in range(len(peaks)-1):
        if ((peaks[i+1] - peaks[i]) > (sample_width*.2)) and ((peaks[i+1] - peaks[i]) < (sample_width*1.8)):
            check_start = i
            check_count = check_count + 1
        else:
            check_start = 0
            check_count = 0
        if check_count > 20:
            new_peaks.append(peaks[check_start])
            print("peak location: "+str(new_peaks))
            #break;

    if len(new_peaks) == 0:
        new_peaks.append(0)


    plt.figure(1)    

    #width = 5512 #sample rate*0.5   #int(abs(new_peaks[0]-new_peaks[1]))
    #width = 2334 #int(math.floor(samplerate*.5))
    #.125 for wav
    width = 4000 #int(math.floor(samplerate/11.9))

    #width = math.floor(int(abs(new_peaks[0]-new_peaks[1])*2))
    #print(width)
    data_hilbert = data_hilbert[:math.floor(len(data_hilbert)/width)*width]
    #data_hilbert = (np.reshape( np.roll(   data_hilbert, new_peaks[0]),   (-1,width))   )
    data_hilbert = np.roll(np.reshape(data_hilbert,(-1,width)), (0,-new_peaks[0]))


    #data_hilbert = (np.reshape( np.roll(   data_hilbert, new_peaks[1]),   (width,-1))   )
    #data_hilbert = (np.reshape(   data_hilbert,   (-1,width))   )
    #data_hilbert = (np.reshape(   data_hilbert,   (width,-1))   )
    reshaped = np.asarray(data_hilbert)

    plt.cla()
    #plt.imshow(reshaped,cmap='gray', vmin = np.amin(data_hilbert)*.01, vmax = np.mean(data_hilbert)*2)
    plt.imshow(reshaped,cmap='gray', vmin = np.mean(data_hilbert)*.8, vmax = np.mean(data_hilbert)*1.3)
    plt.draw()  
    plt.show()
    #plt.show(block=False)
    #plt.pause(0.05)
