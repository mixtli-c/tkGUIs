"""
Script for running the Methods from Control_Examples.py
Uncomment the method you would like to test

R. Sheehan 19 - 9 - 2024
"""

import os
import Control_Examples
import matplotlib.pyplot as plt
import time
import numpy as np

# Where are you? 
pwd = os.getcwd()

print(pwd)

# 0. Basic Find, Open, Close
#Control_Examples.Simple_Open_Close()

# 1. Step through voltages
#Control_Examples.Step_Through_Voltages()

# 2. Basic single channel sweep
#Control_Examples.Simple_Sweep()

# 3. Read all input channels
#Control_Examples.Simple_Sweep_Read_All()

# 4. Differential read
#Control_Examples.Differential_Readings()

# 5. Multi-reads and timings
#Control_Examples.Multiple_Readings()

# 6. Multimeter mode
#Control_Examples.Multimeter_Mode()

# 7. Linear single channel sweep
#Control_Examples.Linear_Sweep_V1()
#Control_Examples.Linear_Sweep_V2()

# 8. Read a waveform
#Control_Examples.Read_Waveform()

# 9. Do a sweep and plot
sweepie = Control_Examples.Linear_Sweep_V4()
res =33
rg = 3.3*(5+(200/33))
i = (sweepie[:,3]-sweepie[:,1])/rg
v2 = (sweepie[:,2]-sweepie[:,1])
v4 = (sweepie[:,5]-sweepie[:,4])
coef2 = np.polyfit(i,v2,1)
poly1d_fn2 = np.poly1d(coef2)
coef4 = np.polyfit(i,v4,1)
poly1d_fn4 = np.poly1d(coef4)
fig = plt.figure(figsize=(8,6))
gs = fig.add_gridspec(1,1)
ax1 = fig.add_subplot(gs[0,0])
#ax1.set_xlim(0,0.09)
ax1.grid()
ax1.plot(i,v2,'.k')
ax1.plot(i,poly1d_fn2(i),'--k',label='coef = %.2f' %coef2[0])
ax1.plot(i,v4,'.b')
ax1.plot(i,poly1d_fn4(i),'--b',label='coef = %.2f' %coef4[0])
ax1.legend()
plt.savefig('plot.jpg')
plt.show()
