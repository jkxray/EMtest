from ophyd import EpicsSignal
import numpy as np
import time
from decimal import Decimal
import os
import sys
import threading
sys.path.append('../')
from Prologix import Prologix

#pv = 'XF:03ID-BI{EM:BPM1}'
pv = 'XF:12IDA-BI:2{EM:BPM1}'
path='../data/005'
port='/dev/ttyUSB1'
data = 'none'
channel = 'none'
averaging_time = 'none' #in seconds
num_points = 100
input_size = 15
saturation_multiplier=1.1
trial_id='0'
values_per_read=50
help_flag=False
for arg in sys.argv:
    if arg.split('=')[0]=='help':
        print('Available parameters are:\npv: PV for electrometer under test. Default is set to '+pv+'\npath: path to save csv files.\nprologix-port: Port path for prologix adapter /dev/???. Default is set to '+port+'\ndata: Data types.')
        help_flag=True
    if arg.split('=')[0]=='pv':
        pv=arg.split('=')[1]
    if arg.split('=')[0]=='path':
        path=arg.split('=')[1]
    if arg.split('=')[0]=='port':
        port=arg.split('=')[1]
    if arg.split('=')[0]=='data':
        data=arg.split('=')[1]
    if arg.split('=')[0]=='channel':
        channel=int(arg.split('=')[1])
    if arg.split('=')[0]=='averaging_time':
        averaging_time=float(arg.split('=')[1])
    if arg.split('=')[0]=='num_points':
        num_points=int(arg.split('=')[1])
    if arg.split('=')[0]=='saturation_multiplier':
        saturation_multiplier=float(arg.split('=')[1])
    if arg.split('=')[0]=='input_size':
        input_size=int(arg.split('=')[1])
    if arg.split('=')[0]=='trial_id':
        trial_id=arg.split('=')[1]
    if arg.split('=')[0]=='values_per_read':
        values_per_read=arg.split('=')[1]
if help_flag==False:
    print('###')
    print('PV is: '+pv)
    print('Data will be saved to: '+path)
    print('Port for prologix adapter is: '+port)
    print('Data type is: '+data)
    time.sleep(0.5)
    EpicsSignal(pv+'Acquire').put(1) #sets mode to acquire
    time.sleep(0.5)
    EpicsSignal(pv+'TS:TSAcquireMode').put(1) #sets to circular buffer
    time.sleep(0.5)
    EpicsSignal(pv+'ValuesPerRead').put(values_per_read) #sets values per read to values_per_read
    time.sleep(0.5)
    EpicsSignal(pv+'AcquireMode').put(0) #sets acquire mode to continuous
    time.sleep(0.5)
    EpicsSignal(pv+'TS:TSAcquire').put(1) #start acquiring
    time.sleep(0.5)
    pro = Prologix(port)


    if data == 'none':
        print('###')
        print('Please provide data type in the parameters by \'data=TYPE\'\nThe available TYPES are:')
        print('bias\ndac\ncurrent\ndrift\noffset')
print("Configuration finished.")
