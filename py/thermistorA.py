import numpy as np
import matplotlib.pyplot as plt
import Control_Examples
import IBM4_Lib
from time import time,sleep

try:
    # instantiate an object that interfaces with the IBM4
    the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

    # this assumes that you are reading the voltage across a resistor and diode in series
    # A2 set to Vin, A3 between the resistor and the diode, A4 at GND
    Nreads = 237
    input_ch = 'A2'
    ground_ch = 'D2'
    #output_ch = 'A0' # select the voltage output channel either A0 or A1

    #the_dev.WriteVoltage(output_ch, 2)
    #readings = the_dev.ReadAverageVoltageAllChnnl(Nreads)
    option = input('Type S to start, E to exit: ')
    if option.lower() == 's':
        for i in range(40):
            reading1 = the_dev.ReadAverageVoltage(input_ch, Nreads)
            reading2 = the_dev.ReadAverageVoltage(ground_ch, Nreads)
            voltage = reading1 - reading2
            temperature = voltage * 3
            print('Voltage: %.2f\tTemperature: %.2f  \r' %(voltage,temperature),end='')
            sleep(0.5)
        print('\n')
    if option.lower() == 'e':
        del the_dev # destructor for the IBM4 object, closes comms
except Exception as e:
    #print(ERR_STATEMENT)
    print(e)
    try:
        del the_dev # destructor for the IBM4 object, closes comms
    except:
        pass
