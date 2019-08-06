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
    #home_position = [0,0,0]


    step_size=0.001 #in mm. 0.005 takes ~ 12 h.
    radius=1 #in mm
    init_pos = np.add(home_position,[-radius,0,-radius])
    positions = []
    for i in range(int(radius*2/step_size + 1)):
        for j in range(int(radius*2/step_size + 1)):
            delta=[step_size*j,0,step_size*i]
            positions.append(np.add(init_pos,delta))
    #print(positions)
    f = open(path+"/scan_"+str(step_size)+"mm.csv","w")
    #out='x,y,z,photodiode (micro amp), current A, current B, current C, current D'
    #f.write(out+'\n')
    for i in range(len(positions)):

        EpicsSignal(pv_motor+'X.VAL').put(positions[i][0])
        EpicsSignal(pv_motor+'Z.VAL').put(positions[i][2])
        if(i%int(radius*2/step_size + 1)==0):
            time.sleep(2)
        else:
            time.sleep(0.3)
        currA=EpicsSignal(pv_EM2+'Current1:MeanValue_RBV').get()
        currB=EpicsSignal(pv_EM2+'Current2:MeanValue_RBV').get()
        currC=EpicsSignal(pv_EM2+'Current3:MeanValue_RBV').get()
        currD=EpicsSignal(pv_EM2+'Current4:MeanValue_RBV').get()
        currPhoto=EpicsSignal(pv_EM1+'Current1:MeanValue_RBV').get()
        currTherm=EpicsSignal(pv_EM1+'Current2:MeanValue_RBV').get()
        timm = time.time()
        print('moved to '+str(positions[i][0]-home_position[0])+', '+str(positions[i][2]-home_position[2]))
        out = str(timm)+', '+str(positions[i][0])+', '+str(positions[i][1])+', '+str(positions[i][2])+', '+str(currPhoto)+', '+str(currTherm)+', '+str(currA)+', '+str(currB)+', '+str(currC)+', '+str(currD)
        print(out)
        f.write(out+'\n')
    f.close()
    EpicsSignal(pv_motor+'X.VAL').put(home_position[0])
    EpicsSignal(pv_motor+'Y.VAL').put(home_position[1])
    EpicsSignal(pv_motor+'Z.VAL').put(home_position[2])
    print("Finished")
