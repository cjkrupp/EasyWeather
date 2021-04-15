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

def read_raw(filename):
    f = open(filename, "rb")
    data = f.read()
    t = list(range(len(data)))

    # Convert continuous stream of data into array of bytes
    data = bytearray(data)
    del data[len(data)-1:]
    # Do the same as above for t
    del t[len(t)-1:]
    # Turn array of bytes into an array of signed words
    data_16bit = array.array('h', data)
    # Because data comes in in reverse order, swap the bytes two by two for each word
    data_16bit.byteswap()

    # Create a new t to match our array of words (shortened to half the size in bytes)
    t = list(range(len(data_16bit)))
    if len(t) != 1:
        print("read_wav(): Successfully read wav file")
  
    #[:,1]
    return t,data_16bit,48000


