#data = [1,2,3,6,5,6,7,8,9,0]
def resample(smpl_rate, desired_smpl, data):  #establish function (will this even work?)
    '''
    x = len(data)        #get the length of our data
    new_data = []        #make a list for new data?
    divisor = round(smpl_rate/desired_smpl)
    i = 0
    j = 0

    while (i+j-1) <= x:
        if j == i:
            new_data.append(data[j])
            i += divisor
        j += 1
    '''
    new_data = [] 
    for i in range(len(data)):
        if (i % (smpl_rate/desired_smpl)) == 0:
            new_data.append(data[i])
    
            
    return new_data
#a = resample(10, 2, data)
#print(a) 
