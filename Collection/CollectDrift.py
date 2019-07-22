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
def drift():
  #DRIFT
  #interval=60*5 #5min between each measurement
  interval = 30 #30s between each measurement spans
  span=25 #time span to take data
  max_time=3600*48 # run for 24 hours

  time_init=time.time()
  out='channel, start time(s), end time (s), voltage mean, voltage std, voltage num, current mean, current std, current num'

  EpicsSignal(pv+'CalibrationMode').put(1)
  EpicsSignal(pv+'CopyADCOffsets.PROC').put(0)
  EpicsSignal(pv+'CalibrationMode').put(0)

  EpicsSignal(pv+'AveragingTime').put(100e-3)
  EpicsSignal(pv+'TS:TSAveragingTime').put(100e-3)
  EpicsSignal(pv+'TS:TSNumPoints').put(1)

  EpicsSignal(pv+'TS:TSAcquireMode').put(0) #sets to circular buffer

  EpicsSignal(pv+'Range').put(0)

  pro.write('sens:volt:rang:auto 1',13)

  with open(path+"/drift."+trial_id+".csv","w") as f:
      f.write(out+'\n')
      counter = 0
      time_init=time.time()
      target_time = time_init+counter*interval
      while time.time() < time_init+max_time:
          if time.time() > target_time:
              counter+=1
              target_time = time_init+counter*interval
              volts=[]
              currentArr=[]
              start_time=0
              end_time=0
              for i in range(1):
                  currentArr.append([])
              def collect(id):
                  while time.time() < start_time+span:
                      if id==0:
                          pro.write("meas:volt:dc?",13)
                          value_measured_orig=pro.readline()
                          value_measured=value_measured_orig.split(',')[0].split('N')[0]
                          try:
                              volts.append(float(value_measured))
                          except:
                              print(value_measured_orig+'.split(\',\')[0].split(\'N\')[0] cannot be converted into a float')
                      if id==1:
                          isAquiring = EpicsSignal(pv+'TS:TSAcquiring').get()
                          if isAquiring == 0: #if it's done acquiring
                              for channel in range(1): #collect data for each channel
                                  curr_str=EpicsSignal(pv+'TS:Current'+str(channel+1)+':TimeSeries').value
                                  #print(str(channel)+' '+str(curr_str))
                                  currentArr[channel].append(curr_str[0])
                              EpicsSignal(pv+'TS:TSAcquire').put(1) #acquire new data

              volt_thread = threading.Thread(target=collect, args=(0,))
              current_thread = threading.Thread(target=collect, args=(1,))
              EpicsSignal(pv+'TS:TSAcquire').put(1) #acquire new data
              start_time=time.time()
              # starting thread 1
              volt_thread.start()
              # starting thread 2
              current_thread.start()

              # wait until thread 1 is completely executed
              volt_thread.join()
              # wait until thread 2 is completely executed
              current_thread.join()
              end_time=time.time()

              voltage_mean = np.average(volts)
              voltage_std = np.std(volts,ddof=1)
              voltage_num = len(volts)


              for channel in range(1):
                  current_mean = np.average(currentArr[channel])
                  current_std = np.std(currentArr[channel],ddof=1)
                  current_num=len(currentArr[channel])
                  out=str(channel)+','+str(start_time)+','+str(end_time)+','+str(voltage_mean)+','+str(voltage_std)+','+str(voltage_num)+','+str(current_mean)+','+str(current_std)+','+str(current_num)
                  print(out)
                  f.write(out+'\n')
              f.flush()

  print('Finished')
