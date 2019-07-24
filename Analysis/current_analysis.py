import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys
from analysis_config import *
def current():
    #CURRENT
    range_values=[1,10,100,1000,50e3]

    for range_value in range_values:
        plt.close()
        for channel in range(4):
            #channel=2
            x = []
            xo=[]
            y = []
            yo=[]
            dy = []
            dyo=[]
            markers= [',', 'x', '+', 'v','^', '<', '>', 's', 'd']
            line=0
            with open(path+'/data/'+ave_time+'ms_current'+str(channel)+'.'+trial_id+'.csv','r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                next(csvfile)
                line+=1
                next(csvfile)
                line+=1
                for row in plots:
                    if len(row)>1:
                        if row[5]=='start':
                            input=float(row[0])*(1e6)
                            mean=float(row[3])
                            std=float(row[4])
                            rng=float(row[1])
                            if rng == range_value:
                                if line%num_points < num_points:
                                    x.append(input)
                                    y.append(mean)
                                    dy.append(std/num_points**0.5)
                                if range_value!=50e3:
                                    if input < range_value:
                                        xo.append(input)
                                        yo.append(mean)
                                        dyo.append(std/num_points**0.5)
                                else:
                                    if input < range_value*0.8:
                                        xo.append(input)
                                        yo.append(mean)
                                        dyo.append(std/num_points**0.5)
                    line+=1
            p, c = np.polyfit(xo, yo, 1, w=dyo, cov=True)
            e = np.sqrt(np.diag(c))
            slope=sci_not(p[0],e[0],True)
            offset=sci_not(p[1],e[1],True)
            #print([p[1],e[1]])
            slope_str= '('+str(slope[0])+'\\pm'+str(slope[1])+')e'+str(slope[2]) if slope[2] != 0 else str(slope[0])+'\\pm'+str(slope[1])
            offset_str= '('+str(offset[0])+'\\pm'+str(offset[1])+')e'+str(offset[2]) if offset[2] != 0 else str(offset[0])+'\\pm'+str(offset[1])
            med_std=sci_not(dyo[round(len(dyo)/2)]*num_points**0.5,dyo[round(len(dyo)/2)]*num_points**0.5,True)
            std_str= str(med_std[0])+'e'+str(med_std[2]) if med_std[2] != 0 else str(med_std[0])
            if channel!=3:
                print(str(channel)+' & '+str(range_value)+' & $'+slope_str+'$ & $'+offset_str+'$ & '+std_str+' \\\\ \\hline')
            else:
                print(str(channel)+' & '+str(range_value)+' & $'+slope_str+'$ & $'+offset_str+'$ & '+std_str+' \\\\ \\Xhline{3\\arrayrulewidth}')
            #\\\\ \\Xhline{3\\arrayrulewidth}

            slope=sci_not(p[0],e[0])
            offset=sci_not(p[1],e[1])

            plt.plot(np.array(x),offset[0]*10**offset[2]+np.array(x)*slope[0]*10**slope[2])
            plt.scatter(x,y, marker=markers[channel],label='channel'+str(channel))

        plt.legend()
        plt.xlabel('Input (\u03bcA)')
        plt.ylabel('Measurement (\u03bcA)')
        plt.title('Ave. Time '+ave_time+'ms, '+'Range '+str(int(range_value)))
        if show_plot=='y':
            plt.show()

        if save_plot=='y':
            plt.savefig(path+'/plot/'+ave_time+'ms_range'+str(int(range_value))+'.png')

    if show_plot=='n':
        print('Not showing plot')
    if save_plot=='n':
        print('not saving plot')
