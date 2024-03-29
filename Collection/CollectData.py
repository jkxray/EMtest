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
import CollectDAC
import Calibrate
import CollectBias
import CollectCurrent
import CollectScan
import CollectScan_Drift2
import CollectBiasScan
if data == 'calibrate':
    Calibrate.calibrate()
elif data == 'bias':
    CollectBias.bias()

elif data == 'dac':
    CollectDAC.dac()

elif data == 'current':
    print('Collecting current.')
    CollectCurrent.current()
elif data == 'scan':
    CollectScan.scan()
elif data=='bias_scan':
    CollectBiasScan.scan()
elif data=='scan_drift2':
    CollectScan_Drift2.scan()
else:
    print("Not supported.")
