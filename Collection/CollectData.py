from ophyd import EpicsSignal
import numpy as np
import matplotlib.pyplot as plt
import time
from decimal import Decimal
import os
import sys
sys.path.append('../')
from Prologix import Prologix

pv = 'XF:12IDA-BI:2{EM:BPM1}'
path='../data/'
port='/dev/ttyUSB6'
data = 'none'
channel = 'none'
averaging_time = 'none'
num_points = 100
input_size = 15
saturation_multiplier=1.2
for arg in sys.argv:
    if arg.split('=')[0]=='help':
        print('Available parameters are:\npv: PV for electrometer under test.\npath: path to save csv files.\nprologix-port: Port path for prologix adapter ("/dev/???")\ndata: Data types.')
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


print('###')
print('PV is: '+pv)
print('Data will be saved to: '+path)
print('Port for prologix adapter is: '+port)
print('Data type is: '+data)

pro = Prologix(port)

if data == 'none':
    print('###')
    print('Please provide data type in the parameters by \'data=TYPE\'\nThe available TYPES are:')
    print('bias\ndac\ncurrent\ndrift')
if data == 'bias':
    #BIAS
    f = open(path+"/bias.csv","w")
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

if data == 'dac':
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


if data == 'current':
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
    print('will approximately take '+str((INPUTS_SIZE*wait_time*len(RANGE_VALUES))/60)+' minutes to complete. The interval between each measurement is '+str(wait_time)+' seconds.')

    time_init=time.time()
    time_now=0

    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}CalibrationMode').put(1)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}CopyADCOffsets.PROC').put(0)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}CalibrationMode').put(0)

    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}AveragingTime').put(AVE_TIME)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}TS:TSAveragingTime').put(AVE_TIME)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}TS:TSNumPoints').put(NUM_POINTS)

    #f = open(path+"Serial#6_ver2/current"+str(channel)+".csv","w")
    out='Input (A), range (micro A), range_rbv, mean, std, start/end\n'

    with open(path+"/"+str(int(AVE_TIME*1000))+"ms_current"+str(CHANNEL)+".csv","w") as f:

        for i in range(len(RANGE_VALUES)):
            inputs=[] #in amps
            for j in range(INPUTS_SIZE):
                inputs.append(RANGE_VALUES[i]*SATURATION_MULTIPLIER*j/(INPUTS_SIZE*1e6))
            #print(inputs)

            for j in range(INPUTS_SIZE):
                print("range: "+str(i)+" input: "+str(inputs[j]))
                EpicsSignal(pv+'Range').put(i)
                input_sci = '%.2E' % Decimal(str(inputs[j]))
                pro.write("sour:curr:ampl "+input_sci,12)

                time_delta=time.time()-time_now-time_init
                time.sleep(wait_time-time_delta)
                time_now=time.time()-time_init

                currentArr=EpicsSignal('XF:12IDA-BI:2{EM:BPM1}TS:Current'+str(CHANNEL+1)+':TimeSeries',name='TS').value
                range_rbv=int(EpicsSignal('XF:12IDA-BI:2{EM:BPM1}Range_RBV').value)
                out+=str(inputs[j])+','+str(RANGE_VALUES[i])+','+str(RANGE_VALUES[range_rbv])+','+str(np.average(currentArr))+','+str(np.std(currentArr,ddof=1))+',start\n'
                for current in currentArr:
                    out+=str(current)+'\n'
                out+=str(inputs[j])+','+str(RANGE_VALUES[i])+','+str(RANGE_VALUES[range_rbv])+','+str(np.average(currentArr))+','+str(np.std(currentArr,ddof=1))+',end\n'                
                f.write(out)
    pro.write("syst:beep:stat on",12)
    pro.write("sour:curr:rang:auto off",12)
    pro.write("output OFF",12)
    pro.write("hi",12) #sends error to 6221 to make it beep when it ends
    print('Finished')
    #f.close()

if data == 'drift':
    #DRIFT

    range_values=[1] #in micro amps (1e-6A)
    interval=60*5 #5min between each measurement
    max_time=3600*48 # run for 48 hours

    time_init=time.time()
    time_now=0
    out='channel, time (s), temperature_voltage mean, temp_voltage std, range (micro A), range_rbv, mean, std'

    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}CalibrationMode').put(1)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}CopyADCOffsets.PROC').put(0)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}CalibrationMode').put(0)

    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}AveragingTime').put(1e-3)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}TS:TSAveragingTime').put(100e-3)
    EpicsSignal('XF:12IDA-BI:2{EM:BPM1}TS:TSNumPoints').put(100)

    pro.write('sens:volt:rang:auto 1',27)

    with open(path+"/drift.csv","w") as f:
        f.write(out+'\n')
        while time_now < max_time:
            for i in range(len(range_values)):
                EpicsSignal(pv+'Range').put(i)
                range_rbv=int(EpicsSignal('XF:12IDA-BI:2{EM:BPM1}Range_RBV').value)
                time_delta=time.time()-time_now-time_init
                time.sleep((interval/len(range_values))-time_delta)
                time_now=time.time()-time_init
                volts=[]
                for j in range(5):
                    pro.write("meas:volt:dc?",27)
                    value_measured=pro.readline()
                    value_measured=value_measured.split(',')[0].split('N')[0]
                    volts.append(float(value_measured))
                for channel in range(4):
                    currentArr=EpicsSignal('XF:12IDA-BI:2{EM:BPM1}TS:Current'+str(channel+1)+':TimeSeries',name='TS').value
                    out=str(channel)+','+str(time_now)+','+str(np.average(volts))+','+str(np.std(volts))+','+str(range_values[i])+','+str(range_values[range_rbv])+','+str(np.average(currentArr))+','+str(np.std(currentArr))
                    f.write(out+'\n')
    print('Finished')
