import platform
import receive_udp
import analysis
import read_wav
import read_raw


platform_path = ""

print("Starting EasyWeather..")
if (platform.system() == "Linux"):
    print("It looks like you are running Linux.")
    platform_path = "rtl_sdr"
    
if (platform.system() == "Windows"):
    print("It looks like you are running Windows.")
    platform_path = "Windows/x64/rtl_sdr.exe"
    
if (platform.system() == "Darwin"):
    print("It looks like you are running MacOS.")
    platform_path = "Macos/MacOS/rtl_sdr"
    

while 1:
    mode = input("\nSelect one of the following modes of operation:\n1. Read data from GQRX / UDP\n2. Read Wav File\n3. Read Raw Data File\n\nEnter a number: \n")
    if (mode == '1'):
        print("Starting UDP capture...\nMake sure to start UDP broadcast on GQRX or SDR Sharp @ 127.0.0.1 port 7355\nPress CTRL-C to quit, otherwise start realtime.py to view live data.")
        t,data,samplerate = receive_udp.receive_data_UDP()
        break
    if (mode == '2'):
        while 1:
            filename = input("\nStarting wav file analysis...\nEnter wav file name: ")
            if (len(filename) != 0):
                t,data,samplerate = read_wav.read_wav(filename)
                analysis.analysis(t,data,samplerate)
                break
        break
    if (mode == '3'):
        while 1:
            filename = input("\nStarting raw file analysis...\nEnter raw file name (.dat): ")
            if (len(filename) != 0):
                print("Reading file: " + str(filename))
                t,data,samplerate = read_raw.read_raw(filename)
                analysis.analysis(t,data,samplerate)
                break
        break
        
