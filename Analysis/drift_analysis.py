import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not

path = '../Tests/Serial6_ver3/'
ranges=[1]
for range_value in ranges:
    x = []
    y = []
    y2=[]
    dy = []
    dy2=[]
    with open(path+'data/drift0.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in plots:
            time=float(row[0])/60/60
            mean=float(row[5])*1e6
            std=float(row[6])*1e6
            v=float(row[1])*1e6
            stdv=float(row[2])*1e6
            if float(row[3]) == range_value:
                x.append(time)
                y.append(mean)
                dy.append(std/(1000**0.5))
                y2.append(v)
                dy2.append(stdv/(5**0.5))

fig=plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212, sharex = ax1)
plt.title('Temperature and Current Drift')
ax1.errorbar(x,y,yerr=dy,fmt='none',ecolor='red')
ax1.plot(x,y)
ax2.set_xlabel('Time (h)')
ax1.set_ylabel('Drift Measurement (pA)')
ax2.errorbar(x,y2,yerr=dy2,fmt='none',ecolor='red')
ax2.plot(x,y2)
ax2.set_ylabel('Temperature Measurement (\u03bcV)')
plt.xlim([0,5])

#plt.show()
plt.savefig(path+'plot/'+'drift0.png')
