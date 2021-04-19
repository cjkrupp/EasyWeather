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
    
    data_16bit = np.fromfile(filename, dtype=np.dtype('<i4') )

    
    # Create a new t to match our array of words (shortened to half the size in bytes)
    t = list(range(len(data_16bit)))
    if len(t) != 1:
        print("read_wav(): Successfully read wav file")
  
    #[:,1]
    return t,data_16bit,48000


