from ophyd import EpicsSignal
import numpy as np
import time
from decimal import Decimal
import os
import sys
import threading
sys.path.append('../')
from Prologix import Prologix


from Configuration import *

def bias():
  #BIAS
    f = open(path+"/bias."+trial_id+".csv","w")
    out='bias,rbv,measured'
    f.write(out+'\n')
    biases=np.arange(-10,11) #array from -10 to 10
    for bias in biases:
        for i in range(3):
            EpicsSignal(pv+'BiasVoltage').put(bias)
            #time.sleep(0.05)
            pro.write("meas:volt:dc?",27)
            value_measured=pro.readline()
            value_RBV=EpicsSignal(pv+'BiasVoltage_RBV').get()
            out=str(bias)+', '+str(value_RBV)+', '+value_measured.split(',')[0].split('N')[0]
            print(out)
            f.write(out+'\n')
    f.close()
    print('Finished')
