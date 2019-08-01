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
def scan():
    pv_EM1 = 'quadEMTest:NSLS_EM:'
    pv_motor = 'RGD:'
    pv_EM2 = 'XF:12IDA-BI:2{EM:BPM1}'
    home_position = [25.05,-10,38.808]
    biases=[]
    for i in range(50):
        biases.append(-10+20*i/50)
    position=np.add(home_position,[-1,0,-1])
    EpicsSignal(pv_motor+'X.VAL').put(position[0])
    EpicsSignal(pv_motor+'Z.VAL').put(position[2])
    f = open(path+"/bias_scan.csv","w")
    for bias in biases:
        EpicsSignal(pv_EM2+'BiasVoltage').put(bias)
        value_RBV=EpicsSignal(pv_EM2+'BiasVoltage_RBV').get()
        time.sleep(0.3)
        currA=EpicsSignal(pv_EM2+'Current1:MeanValue_RBV').get()
        currB=EpicsSignal(pv_EM2+'Current2:MeanValue_RBV').get()
        currC=EpicsSignal(pv_EM2+'Current3:MeanValue_RBV').get()
        currD=EpicsSignal(pv_EM2+'Current4:MeanValue_RBV').get()
        currPhoto=EpicsSignal(pv_EM1+'Current1:MeanValue_RBV').get()
        out=str(bias)+', '+str(value_RBV)+', '+str(currPhoto)+', '+str(currA)+', '+str(currB)+', '+str(currC)+', '+str(currD)
        print(out)
        f.write(out+'\n')
    f.close()
    EpicsSignal(pv_motor+'X.VAL').put(home_position[0])
    EpicsSignal(pv_motor+'Y.VAL').put(home_position[1])
    EpicsSignal(pv_motor+'Z.VAL').put(home_position[2])
    print("Finished")
