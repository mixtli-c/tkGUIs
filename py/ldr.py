import numpy as np
import matplotlib.pyplot as plt
from time import time,sleep
import Control_Examples
import IBM4_Lib

try:
    # instantiate an object that interfaces with the IBM4
    the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

    # this assumes that you are reading the voltage across a resistor and diode in series
    # A2 set to Vin, A3 between the resistor and the diode, A4 at GND
    Nreads = 237
    input_ch = 'A2'
    ground_ch = 'D2'
    output_ch_cc = 'A1' # select the voltage output channel either A0 or A1
    output_ch_nl = 'A0'
    led = 0
    the_dev.WriteVoltage(output_ch_cc, .7)
    the_dev.WriteVoltage(output_ch_nl, led)
    #readings = the_dev.ReadAverageVoltageAllChnnl(Nreads)
    while True:
        option = input('Type L to switch LED on/off, S to start, E to exit: ')
        if option.lower() == 'l':
            if led == 0:
                print('Turning on')
                led = 3
            elif led == 3:
                print('Turning off')
                led = 0
            the_dev.WriteVoltage(output_ch_nl, led)
        elif option.lower() == 's':
            for i in range(40):
                reading1 = the_dev.ReadAverageVoltage(input_ch, Nreads)
                reading2 = the_dev.ReadAverageVoltage(ground_ch, Nreads)
                voltage = reading1 - reading2
                if voltage < 1:
                    status = '0'
                elif voltage > 2:
                    status = '1'
                else:
                    status = '?'
                temperature = voltage * 3
                print('Voltage: %.2f\tStatus: %s  \r' %(voltage,status),end='')
                sleep(0.55)
            print('', end='\n')
        elif option.lower() == 'e':
            del the_dev # destructor for the IBM4 object, closes comms
            break
except Exception as e:
    #print(ERR_STATEMENT)
    print(e)
    try:
        del the_dev # destructor for the IBM4 object, closes comms
    except:
        pass
