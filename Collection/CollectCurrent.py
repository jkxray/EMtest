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

def current():
  print('###')
  print('channel is '+str(channel))
  print('averaging time is '+str(averaging_time))

  if channel=='none':
      print('please provide channel')
      sys.exit()
  if averaging_time=='none':
      print('please provide averaging_time')
      sys.exit()
  #CURRENT
  CHANNEL=channel
  RANGE_VALUES=[1,10,100,1e3,50e3] #in micro amps (1e-6A)
  inputs=[] #in amps
  pro.write("output ON",12)
  pro.write("sour:curr:rang:auto on",12)
  pro.write("syst:beep:stat off",12)

  INPUTS_SIZE=input_size
  SATURATION_MULTIPLIER=saturation_multiplier
  AVE_TIME=averaging_time
  NUM_POINTS=num_points

  wait_time=AVE_TIME*NUM_POINTS+5
  print('The interval between each measurement is '+str(wait_time)+' seconds.')
  print('Will approximately take '+str((INPUTS_SIZE*wait_time*len(RANGE_VALUES))/60)+' minutes to complete.')
  print('---------------------------------------')
  time_init=time.time()
  time_now=0


  EpicsSignal(pv+'AveragingTime').put(AVE_TIME)
  time.sleep(1)
  EpicsSignal(pv+'TS:TSAveragingTime').put(AVE_TIME)
  time.sleep(1)
  EpicsSignal(pv+'TS:TSNumPoints').put(NUM_POINTS)
  time.sleep(1)
  #sys.exit()
  #f = open(path+"Serial#6_ver2/current"+str(channel)+".csv","w")
  out='Input (A), range (micro A), range_rbv, mean, std, start/end\n'

  with open(path+"/"+str(int(AVE_TIME*1000))+"ms_current"+str(CHANNEL)+".csv","w") as f:
      f.write(out)
      for i in range(len(RANGE_VALUES)):
          inputs=[] #in amps
          for j in range(INPUTS_SIZE+1):
              input = RANGE_VALUES[i]*SATURATION_MULTIPLIER*j/(INPUTS_SIZE*1e6)
              inputs.append(input)
          #print(inputs)

          for j in range(INPUTS_SIZE):

              EpicsSignal(pv+'Range').put(i)
              input_sci = '%.2E' % Decimal(str(inputs[j]))
              pro.write("sour:curr:ampl "+input_sci,12)

              time_delta=time.time()-time_now-time_init
              time.sleep(wait_time-time_delta)
              time_now=time.time()-time_init

              currentArr=EpicsSignal(pv+'TS:Current'+str(CHANNEL+1)+':TimeSeries',name='TS').value
              range_rbv=int(EpicsSignal(pv+'Range_RBV').value)
              out=str(inputs[j])+','+str(RANGE_VALUES[i])+','+str(RANGE_VALUES[range_rbv])+','+str(np.average(currentArr))+','+str(np.std(currentArr,ddof=1))+',start\n'
              print("range: "+str(RANGE_VALUES[i])+" input: "+str(inputs[j]*1e6)+" measured: "+str(np.average(currentArr)))
              for current in currentArr:
                  out+=str(current)+'\n'
              out+=str(inputs[j])+','+str(RANGE_VALUES[i])+','+str(RANGE_VALUES[range_rbv])+','+str(np.average(currentArr))+','+str(np.std(currentArr,ddof=1))+',end\n'
              #print(out)
              f.write(out)
  pro.write("syst:beep:stat on",12)
  pro.write("sour:curr:rang:auto off",12)
  pro.write("output OFF",12)
  pro.write("hi",12) #sends error to 6221 to make it beep when it ends
  print('Finished')
  #f.close()
