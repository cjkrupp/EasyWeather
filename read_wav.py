import socket
import matplotlib.pyplot as plt
import time
import struct

import numpy as np
from scipy import fftpack
import scipy.signal
from scipy import signal
import array
#import resample as rs
import math
import pandas as pd
from scipy.io import wavfile

def read_wav(filename):
    print("read_wav(): Reading data from wav file: "+str(filename))
    samplerate, data = wavfile.read(filename)

    # Create a new t to match our array of words (shortened to half the size in bytes)
    t = list(range(len(data)))
    if len(t) != 1:
        print("read_wav(): Successfully read wav file")
  
    # Check to see if this is a stereo wav or not
    if (data.ndim) > 1:
        return t,data[:,1],samplerate
    else:
        return t,data,samplerate


