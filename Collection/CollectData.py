from ophyd import EpicsSignal
import numpy as np
import matplotlib.pyplot as plt
import time
from decimal import Decimal
import os
import sys
import threading
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
trial_id='0'
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
if help_flag==False:
    print('###')
    print('PV is: '+pv)
    print('Data will be saved to: '+path)
    print('Port for prologix adapter is: '+port)
    print('Data type is: '+data)
    EpicsSignal(pv+'Acquire').put(1) #sets mode to acquire
    EpicsSignal(pv+'TS:TSAcquireMode').put(1) #sets to circular buffer
    EpicsSignal(pv+'ValuesPerRead').put(50) #sets values per read to 50
    EpicsSignal(pv+'AcquireMode').put(0) #sets acquire mode to continuous
    EpicsSignal(pv+'TS:TSAcquire').put(1) #start acquiring
    pro = Prologix(port)


    if data == 'none':
        print('###')
        print('Please provide data type in the parameters by \'data=TYPE\'\nThe available TYPES are:')
        print('bias\ndac\ncurrent\ndrift\noffset')
if data == 'calibrate':
    EpicsSignal(pv+'CalibrationMode').put(1)
    EpicsSignal(pv+'CopyADCOffsets.PROC').put(0)
    EpicsSignal(pv+'CalibrationMode').put(0)
    print('ADC offsets are calibrated')

if data == 'offset':
    f=open(path+"/"+pv+"offsets.csv","w")
    for i in range(4):
        offset=EpicsSignal(pv+'ADCOffset'+str(i+1)).get()
        f.write(str(offset))
        print(offset)
    f.close()
    print('Finished')
if data == 'bias':
    #BIAS
    f = open(path+"/bias."+trial_id+".csv","w")
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
    f = open(path+"/dac"+str(channel)+"."+trial_id+".csv","w")
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


    EpicsSignal(pv+'CalibrationMode').put(1)
    EpicsSignal(pv+'CopyADCOffsets.PROC').put(0)
    EpicsSignal(pv+'CalibrationMode').put(0)

    EpicsSignal(pv+'AveragingTime').put(AVE_TIME)
    EpicsSignal(pv+'TS:TSAveragingTime').put(AVE_TIME)
    EpicsSignal(pv+'TS:TSNumPoints').put(NUM_POINTS)

    #f = open(path+"Serial#6_ver2/current"+str(channel)+".csv","w")
    out='Input (A), range (micro A), range_rbv, mean, std, start/end\n'

    with open(path+"/"+str(int(AVE_TIME*1000))+"ms_current"+str(CHANNEL)+"."+trial_id+".csv","w") as f:

        for i in range(len(RANGE_VALUES)):
            inputs=[] #in amps
            for j in range(INPUTS_SIZE):
                inputs.append(RANGE_VALUES[i]*SATURATION_MULTIPLIER*j/(INPUTS_SIZE*1e6))
            #print(inputs)

            for j in range(INPUTS_SIZE):
                print("range: "+str(RANGE_VALUES[i])+" input: "+str(inputs[j]*1e6))
                EpicsSignal(pv+'Range').put(i)
                input_sci = '%.2E' % Decimal(str(inputs[j]))
                pro.write("sour:curr:ampl "+input_sci,12)

                time_delta=time.time()-time_now-time_init
                time.sleep(wait_time-time_delta)
                time_now=time.time()-time_init

                currentArr=EpicsSignal(pv+'TS:Current'+str(CHANNEL+1)+':TimeSeries',name='TS').value
                range_rbv=int(EpicsSignal(pv+'Range_RBV').value)
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
