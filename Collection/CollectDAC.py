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
def dac():
  print('###')
  print('channel is '+str(channel))
  if channel=='none':
      print('please provide channel')
      sys.exit()
  #DAC
  f = open(path+"/dac"+str(channel)+".csv","w")
  out='set,measured'
  f.write(out+'\n')
  dacs=np.arange(-10,11) #array from -10 to 10
  for dac in dacs:
      for i in range(3):
          EpicsSignal(pv+'DAC'+str(channel)).put(dac)
          #time.sleep(0.05)
          pro.write("meas:volt:dc?",27)
          value_measured=pro.readline()
          out=str(dac)+', '+value_measured.split(',')[0].split('N')[0]
          print(out)
          f.write(out+'\n')
      EpicsSignal(pv+'DAC'+str(channel)).put(0)
  f.close()
  print('Finished')
