import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys
import pandas as pd
def scan(path):
    i=0
    x=0
    y=-1
    out=''

    fluxrr_pd=[]
    fluxrr_d=[]
    fluxrr_d_temp=[]

    z_epics_arr=[]
    Gzs=[]
    z_contrasts=[]

    x_epics_arr=[]
    Gxs=[]
    x_contrasts=[]
    temp_z=0
    colnames=['X', 'Y', 'Z','PD','A','B','C','D']
    data = pd.read_csv(path+'/scan_0.005mm.csv', names=colnames, header=None)
    print(data.describe())
    with open(path+'/scan_0.005mm.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')

        for row in plots:
            x_epics=float(row[0])
            y_epics=float(row[1])
            z_epics=float(row[2])
            pd=float(row[3])
            A=float(row[4])/1e6
            B=float(row[5])/1e6
            C=float(row[6])/1e6
            D=float(row[7])/1e6
            sum=A+B+C+D
            x=i%201
            if x==0:
                y+=1

            flux_pd=pd*1e9/266.4e-9
            fluxrr_pd.append(flux_pd)
            flux_d=0.99122*sum*266.4e-9/pd
            fluxrr_d.append(flux_d)
            fluxrr_d_temp.append(0.99122*sum*1e9)
            #print(flux_d)
            z_epics_arr.append(z_epics)
            Gz=(z_epics)*sum/((C+D)-(A+B))
            Gzs.append(Gz)
            z_contrasts.append(((C+D)-(A+B))/sum)

            x_epics_arr.append(x_epics)
            Gx=(x_epics)*sum/((A+D)-(B+C))
            Gxs.append(Gx)
            x_contrasts.append(((A+D)-(B+C))/sum)

            i+=1
    pdflux=np.mean(fluxrr_pd)
    dflux=np.mean(fluxrr_d)
    #print(sci_not(pdflux,np.std(fluxrr_pd)/(len(fluxrr_pd)**0.5)))
    print(pdflux)
    print(dflux)
    print(np.mean(Gzs))
    print(np.mean(Gxs))
    print(z_epics_arr[0])
    print(z_epics_arr[len(z_epics_arr)-1])
    print(x_epics_arr[0])
    print(x_epics_arr[len(x_epics_arr)-1])
    #plt.scatter(np.array(x_epics_arr)-25.05,Gxs)
    #plt.scatter(np.array(z_epics_arr)-38.808,Gzs)
    plt.scatter(np.array(z_epics_arr)-38.808,z_contrasts)
    plt.scatter(np.array(x_epics_arr)-25.05,x_contrasts)
    plt.show()
