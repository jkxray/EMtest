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
  EpicsSignal(pv+'CalibrationMode').put(1)
  time.sleep(1)
  EpicsSignal(pv+'CopyADCOffsets.PROC').put(0)
  time.sleep(1)
  EpicsSignal(pv+'CalibrationMode').put(0)
  time.sleep(1)
  try:
      with open(path+"/offsets.csv", "r") as f:
          print('Offset file already exists.')
          i=0
          for line in f:
               if i<=3:
                    EpicsSignal(pv+'ADCOffset'+str(i+1)).put(line.strip())
                    print('Setting ADCOffset '+str(i+1)+' to '+line.strip()+'.')
               i+=1
  except Exception as e:
      print(e)
      print('Offset file does not exist. Calibrating.')
      f=open(path+"/offsets.csv","w")
      for i in range(4):
          offset=EpicsSignal(pv+'ADCOffset'+str(i+1)).get()
          f.write(str(offset)+'\n')
          print('offset '+str(i)+': '+str(offset))
      f.close()

  print('Finished')
