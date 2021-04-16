import platform
import receive_udp
import analysis
import read_wav
import read_raw

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

#val = input("Enter which satellite to capture: ") 
print("Starting EasyWeather..")
#t,data,samplerate = receive_udp.receive_data_UDP(60*5,'test')
#t,data,samplerate = read_wav.read_wav('argentina.wav')
#t,data,samplerate = read_wav.read_wav('gqrx_20210416_060338_24525000.wav')
t,data,samplerate = read_raw.read_raw('radio_capture8.dat')

analysis.analysis(t,data,samplerate)
