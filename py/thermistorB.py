import numpy as np
import matplotlib.pyplot as plt
import Control_Examples
import IBM4_Lib
from time import time,sleep
from scipy.optimize import least_squares

def gendata(t,a,b,c):
    '''
    Generates the exponential fit
    '''
    return a+b*np.exp(t*c)

def funct(x,t,y):
    '''
    Function to fit with optimize.least_squares
    '''
    return x[0] + x[1]*np.exp(x[2]*t)-y


try:
    # instantiate an object that interfaces with the IBM4
    the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

    # this assumes that you are reading the voltage across a resistor and diode in series
    # A2 set to Vin, A3 between the resistor and the diode, A4 at GND
    Nreads = 237

    #i_ch_txt = input('Select input channel: ')
    #input_ch = i_ch_txt
    input_ch = 'A2'
    ground_ch = 'D2'
    output_ch = 'A0' # select the voltage output channel either A0 or A1
    input('Press any key to turn on LED.')
    the_dev.WriteVoltage(output_ch, 3)
    input('Press any key to start data collection.')
    the_dev.WriteVoltage(output_ch, 0)
    print('Waiting a bit before collection')
    sleep(30)
    t0= time()
    times = []
    volt = []
    for i in range(600):
        reading1 = the_dev.ReadAverageVoltage(input_ch, Nreads)
        reading2 = the_dev.ReadAverageVoltage(ground_ch, Nreads)
        voltage = reading1 - reading2
        secs = time()-t0
        print('Time (s): %.1f\tVoltage: %.2f  \r' %(secs,voltage),end='')
        times.append(secs)
        volt.append(voltage)
        sleep(0.25)
    print('\n')
    #readings = the_dev.ReadAverageVoltageAllChnnl(Nreads)
    #reading = the_dev.ReadAverageVoltage(input_ch, Nreads)
    # TRF

    x0 = np.array([0,2,-2])
    res_log = least_squares(funct,x0, ftol=1e-12,xtol=1e-12,gtol=1e-12,
                            loss = 'cauchy', f_scale=0.1, args=(np.asarray(times),np.asarray(volt)))

    # The results
    xs = res_log.x
    fit = gendata(np.asarray(times),*xs)
    #### END OF LEAST SQUARES
    plt.plot(times,volt,'-k')
    plt.plot(times,fit,'--r')
    plt.show()
    del the_dev # destructor for the IBM4 object, closes comms
except Exception as e:
    #print(ERR_STATEMENT)
    print(e)
    try:
        del the_dev # destructor for the IBM4 object, closes comms
    except:
        pass
