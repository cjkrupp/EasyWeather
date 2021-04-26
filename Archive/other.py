import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
fs, data = wav.read('/home/owl/gqrx_20210317_202242_99500700.wav')
data_crop = data[20*fs:21*fs]
plt.figure(figsize=(12,4))


resample = 4
data = data[::resample]
fs = fs//resample

def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope

data_am = hilbert(data)


plt.plot(data_am)
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.title("Signal")
plt.show() 
