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
def calibrate():
  time.sleep(0.5)
  EpicsSignal(pv+'CalibrationMode').put(1)
  time.sleep(0.5)
  EpicsSignal(pv+'CopyADCOffsets.PROC').put(0)
  time.sleep(0.5)
  EpicsSignal(pv+'CalibrationMode').put(0)
  time.sleep(0.5)
  print('ADC offsets are calibrated')
  f=open(path+"/"+pv+"offsets.csv","w")
  for i in range(4):
      offset=EpicsSignal(pv+'ADCOffset'+str(i+1)).get()
      f.write(str(offset))
      print('offset '+str(i)+': '+str(offset))
  f.close()
  print('Finished')
