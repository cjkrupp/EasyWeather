import math
from scipy import signal

def resample(smpl_rate, desired_smpl, data): 

    new_data = [] 
    
    number_samples = round(len(data) * float(desired_smpl) / smpl_rate)
    new_data = signal.resample(data, number_samples)
            
    return new_data

