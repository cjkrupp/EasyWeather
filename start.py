import platform
import receive_udp

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



# Returns array of 16 bit values from UDP server
data = receive_udp.receive_data_UDP()

print(data)
