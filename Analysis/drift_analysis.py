import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys

path = '../Tests/Serial006/'
type=0
for arg in sys.argv:
    if arg.split('=')[0]=='type':
        type=int(arg.split('=')[1])
    if arg.split('=')[0]=='path':
        path=arg.split('=')[1]
print('Path is set to '+path)
 
ranges=[1]
if type==0:
    fig=plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex = ax1)
    ax2.set_xlabel('Time (h)')
    ax1.set_ylabel('Drift Measurement (pA)')
    ax2.set_ylabel('Temperature Measurement (\u03bcV)')

for range_value in ranges:
    t = []
    dt = []
    i = []
    di = []
    v = []
    dv = []
    with open(path+'data/drift.1.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in plots:
            time=((float(row[1])+float(row[2]))/2 - 1562188231.7851243)/60/60
            #if time>15 and time<25:
            t.append(time)
            dt.append((float(row[2])-float(row[1]))/2/60/60)
            i.append(float(row[6])*1e6)
            di.append(float(row[7])*1e6/(float(row[8])**0.5))
            v.append(float(row[3])*1e6)
            dv.append(float(row[4])*1e6/(float(row[5])**0.5))
colors=[]
for tm in t:
    colors.append(tm/t[len(t)-1])
if type==0:
    '''
    ax1.errorbar(t,i,xerr=dt,yerr=di,fmt='none',ecolor='red')
    ax1.plot(t,i)
    ax2.errorbar(t,v,xerr=dt,yerr=dv,fmt='none',ecolor='red')
    ax2.plot(t,v)
    ax1.legend()
    '''
    ax1.scatter(t,i,c=colors,cmap='inferno',s=5)
    ax2.scatter(t,v,c=colors,cmap='inferno',s=5)

if type==1:
    #plt.errorbar(i,v,xerr=di,yerr=dv,fmt='none',ecolor=colors)
    plt.scatter(v,i,c=colors,cmap='inferno',s=10)
plt.legend()
plt.title('Temperature and Current Drift')
#plt.show()
plt.savefig(path+'plot/'+'drift'+str(type)+'.png')
