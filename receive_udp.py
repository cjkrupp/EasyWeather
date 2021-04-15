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
import os
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
#                       (seconds)
def receive_data_UDP(capture_time,filename):
    # localhost
    UDP_IP = "127.0.0.1"

    # GQRX default port
    UDP_PORT = 7355

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    # initialize as a byte
    data = b'0'

    data_times = 1024

    #f = open(filename, "wb")
    i = 0
    while os.path.exists("radio_capture%s.dat" % i):
        i += 1

    f = open("radio_capture%s.dat" % i, "ab")
    
    time_end = time.time() + capture_time
    while time.time() < time_end:
    #while data_times >= 0:
        data_temp, addr = sock.recvfrom(1024) # buffer size of 1024 bytes
        #data = data + data_temp
        f.write(data_temp)
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

    
    #print(len(data))
    #print('='+str(len(data))+'h')

    # Turn array of bytes into an array of signed words
    data_16bit = array.array('h', data)
    # Because data comes in in reverse order, swap the bytes two by two for each word
    data_16bit.byteswap()
    
    data_16bit = data #[:,1]
    print(data)
    

    t = list(range(len(data_16bit)))
    
   
    
    return data_16bit


