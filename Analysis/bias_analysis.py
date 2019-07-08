import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
path = '../data/Serial102/'
#BIAS
x = []
y = []
dy = []
line=1
measured_values=[]
markers= ['.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd']
for arg in sys.argv:
    if arg.split('=')[0]=='path':
        path=arg.split('=')[1]
print('Path is set to '+path)
 
with open(path+'bias.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(csvfile)
    for row in plots:
        measured_values.append(float(row[2]))
        if line % 3 == 0:
            set_value=float(row[0])
            x.append(set_value)
            y.append(np.average(measured_values))
            dy.append(np.std(measured_values,ddof=1)/3**0.5)
            #print([set_value,np.average(measured_values),np.std(measured_values,ddof=1)])
            measured_values=[]
        line+=1
    plt.scatter(x,y)
    p, c = np.polyfit(x, y, 1, w=dy, cov=True)
    e = np.sqrt(np.diag(c))
    slope=sci_not(p[0],e[0])
    offset=sci_not(p[1],e[1])
    plt.plot(np.array(x),offset[0]*10**offset[2]+np.array(x)*slope[0]*10**slope[2])
    slope=sci_not(p[0],e[0],True)
    offset=sci_not(p[1],e[1],True)
    slope_str= '('+str(slope[0])+'\\pm'+str(slope[1])+')e'+str(slope[2]) if slope[2] != 0 else str(slope[0])+'\\pm'+str(slope[1])
    offset_str= '('+str(offset[0])+'\\pm'+str(offset[1])+')e'+str(offset[2]) if offset[2] != 0 else str(offset[0])+'\\pm'+str(offset[1])
    med_std=sci_not(dy[2]*3**0.5,dy[2]*3**0.5,True)
    std_str= str(med_std[0])+'e'+str(med_std[2]) if med_std[2] != 0 else str(med_std[0])
    print('$'+slope_str+'$ & $'+offset_str+'$ & '+std_str+'\\\\ \\hline')
plt.legend()
plt.xlabel('Set (V)')
plt.ylabel('Measurement (V)')
#plt.axis([-11, 11, -0.004, 0.003])
plt.title('Bias Output')
plt.show()
#plt.savefig(path+'plot/bias.png')
