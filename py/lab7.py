import os
import Control_Examples
import numpy

# Where are you?
pwd = os.getcwd()

print(pwd)
vins = [0.7,1.3,1.9,2.5,3.1]
rb= 4660
rc= 17
for ele in vins:
    print('Vin set to:',ele)
    data=Control_Examples.Linear_Sweep_V3(ele)
    print(data)
    vb=data[:,1]-data[:,2]
    ib=vb/rb
    vc=data[:,3]-data[:,4]
    ic=vc/rc
    vce=data[:,4]-data[:,5]
    numpy.savetxt('plotNPN'+str(ele)+'.txt',numpy.column_stack((vce,ic,ib)))
