import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys
#import pandas as pd
def scan_z(path):
    i=0
    x=0
    y=-1
    out=''
    size=401
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
    #colnames=['X', 'Y', 'Z','PD','A','B','C','D']
    #data = pd.read_csv(path+'/scan_0.005mm.csv', names=colnames, header=None)
    #print(data.describe())
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
            x=i%size
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
            z_contrasts.append( ((C+D)-(A+B)) / (A+B+C+D) )

            x_epics_arr.append(x_epics)
            Gx=(x_epics)*sum/((A+D)-(B+C))
            Gxs.append(Gx)
            x_contrasts.append(((A+D)-(B+C))/sum)

            i+=1
    #print(z_contrasts)
    pdflux=np.mean(fluxrr_pd)
    dflux=np.mean(fluxrr_d)
    #print(sci_not(pdflux,np.std(fluxrr_pd)/(len(fluxrr_pd)**0.5)))
    print('pdflux: '+str(pdflux))
    print('dflux: '+str(dflux))
    #plt.scatter(np.array(x_epics_arr)-25.05,Gxs)
    #plt.scatter(np.array(z_epics_arr)-38.808,Gzs)
    z_epics_sqr_arr=[]
    z_contrasts_sqr=[]
    #slice 1 dimensional array into 2 dimensional array by rows
    for i in range(size):
        z_epics_sqr_arr.append(z_epics_arr[i*size:(i+1)*size])
        z_contrasts_sqr.append(z_contrasts[i*size:(i+1)*size])
    #rotate matrix so it's sliced by columns
    z_epics_sqr_arr=np.rot90(z_epics_sqr_arr)
    z_contrasts_sqr=np.rot90(z_contrasts_sqr)


    z_epics_sqr_arr_cropped=[]
    z_contrasts_sqr_cropped=[]
    #set offset for every column
    for i in range(size):
        offset=0
        for j in range(size):
            if z_contrasts_sqr[i][j] < 1.5 and z_contrasts_sqr[i][j] > -1.5:

                offset=z_epics_sqr_arr[i][j]+0.01
                #print(offset)
                break
        z_epics_sqr_arr[i]=np.array(z_epics_sqr_arr[i])-offset


    #crop z data and align
    for i in range(len(z_epics_sqr_arr)):
        z_epics_sqr_arr_cropped.append([])
        z_contrasts_sqr_cropped.append([])
        z_count=0
        for j in range(len(z_epics_sqr_arr[i])):
            lim=0.1001
            if z_epics_sqr_arr[i][j]>-1*lim and z_epics_sqr_arr[i][j]<1*lim:
                z_epics_sqr_arr_cropped[i].append(z_epics_sqr_arr[i][j])
                z_contrasts_sqr_cropped[i].append(z_contrasts_sqr[i][j])
        z_epics_sqr_arr_cropped[i]=np.array(z_epics_sqr_arr_cropped[i])
        z_contrasts_sqr[i]=np.array(z_contrasts_sqr[i])
    z_epics_arr_average=[]
    z_contrasts_average=[]
    z_contrasts_stds=[]
    #create 1 dimensional array of each row averaged
    z_epics_sqr_arr_cropped_temp=np.rot90(z_epics_sqr_arr_cropped,3)
    z_contrasts_sqr_cropped_temp=np.rot90(z_contrasts_sqr_cropped,3)
    for i in range(len(z_epics_sqr_arr_cropped_temp)):
        if np.median(z_epics_sqr_arr_cropped_temp[i])>=-0.015 and np.median(z_epics_sqr_arr_cropped_temp[i])<=0.015:
            z_epics_arr_average.append(np.median(z_epics_sqr_arr_cropped_temp[i]))
            z_contrasts_average.append(np.mean(z_contrasts_sqr_cropped_temp[i]))

            z_contrasts_stds.append(np.std(z_contrasts_sqr_cropped_temp[i]))
    #create color gradient
    color=[]
    half = int(size/2)
    for i in range(half):
        color.append((i/half,0,50/255,0.1))
    for i in range(size-half):
        color.append((1,float(i)/(size-half),50/255,0.1))
    #plot each column
    for i in range(size):
        plt.scatter(np.array(z_epics_sqr_arr_cropped[i]),z_contrasts_sqr_cropped[i],c=color[i])
    plt.scatter(z_epics_arr_average,z_contrasts_average,c='blue')

    p, c = np.polyfit(z_epics_arr_average, z_contrasts_average, 1, w=z_contrasts_stds, cov=True)
    e = np.sqrt(np.diag(c))
    #print([p,c,e])
    #print([p[0],e[0]])

    slope=sci_not(p[0],e[0],True)
    offset=sci_not(p[1],e[1],True)
    slope_str= '('+str(slope[0])+'+/-'+str(slope[1])+')e'+str(slope[2]) if slope[2] != 0 else str(slope[0])+'+/-'+str(slope[1])
    print('Gz: '+slope_str)

    slope=sci_not(p[0],e[0])
    offset=sci_not(p[1],e[1])
    plt.plot(np.array(z_epics_arr_average),offset[0]*float(10)**offset[2]+np.array(z_epics_arr_average)*slope[0]*float(10)**slope[2],label='Gz: '+slope_str)
        #plt.scatter(np.array(x_epics_sqr_arr[i])-25.05,x_contrasts_sqr[i],c=color[i])
    plt.xlabel("Z position (mm)")
    plt.ylabel("Z contrast")
    plt.legend()
    plt.show()


def scan_x(path):
    i=0
    x=0
    y=-1
    out=''
    size=401
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
    #colnames=['X', 'Y', 'Z','PD','A','B','C','D']
    #data = pd.read_csv(path+'/scan_0.005mm.csv', names=colnames, header=None)
    #print(data.describe())
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
            x=i%size
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
    print('pdflux: '+str(pdflux))
    print('dflux: '+str(dflux))
    #plt.scatter(np.array(x_epics_arr)-25.05,Gxs)
    #plt.scatter(np.array(z_epics_arr)-38.808,Gzs)
    x_epics_sqr_arr=[]
    x_contrasts_sqr=[]
    #slice 1 dimensional array into 2 dimensional array by rows
    for i in range(size):
        x_epics_sqr_arr.append(x_epics_arr[i*size:(i+1)*size])
        x_contrasts_sqr.append(x_contrasts[i*size:(i+1)*size])


    x_epics_sqr_arr_cropped=[]
    x_contrasts_sqr_cropped=[]
    #set offset for every column
    for i in range(size):
        offset=0
        for j in range(size):
            if x_contrasts_sqr[i][j] < 1.5 and x_contrasts_sqr[i][j] > -1.5:

                offset=x_epics_sqr_arr[i][j]+0.01
                #print(offset)
                break
        x_epics_sqr_arr[i]=np.array(x_epics_sqr_arr[i])-offset


    #crop z data and align
    for i in range(len(x_epics_sqr_arr)):
        x_epics_sqr_arr_cropped.append([])
        x_contrasts_sqr_cropped.append([])
        for j in range(len(x_epics_sqr_arr[i])):
            lim=0.1001
            if x_epics_sqr_arr[i][j]>-1*lim and x_epics_sqr_arr[i][j]<1*lim:
                x_epics_sqr_arr_cropped[i].append(x_epics_sqr_arr[i][j])
                x_contrasts_sqr_cropped[i].append(x_contrasts_sqr[i][j])
        x_epics_sqr_arr_cropped[i]=np.array(x_epics_sqr_arr_cropped[i])
        x_contrasts_sqr[i]=np.array(x_contrasts_sqr[i])
    x_epics_arr_average=[]
    x_contrasts_average=[]
    x_contrasts_stds=[]
    #create 1 dimensional array of each row averaged
    x_epics_sqr_arr_cropped_temp=np.rot90(x_epics_sqr_arr_cropped,1)
    x_contrasts_sqr_cropped_temp=np.rot90(x_contrasts_sqr_cropped,1)
    for i in range(len(x_epics_sqr_arr_cropped_temp)):
        if np.median(x_epics_sqr_arr_cropped_temp[i])>=-0.015 and np.median(x_epics_sqr_arr_cropped_temp[i])<=0.015:
            x_epics_arr_average.append(np.median(x_epics_sqr_arr_cropped_temp[i]))
            x_contrasts_average.append(np.mean(x_contrasts_sqr_cropped_temp[i]))

            x_contrasts_stds.append(np.std(x_contrasts_sqr_cropped_temp[i]))
    #create color gradient
    color=[]
    half = int(size/2)
    for i in range(half):
        color.append((i/half,0,50/255,0.1))
    for i in range(size-half):
        color.append((1,float(i)/(size-half),50/255,0.1))
    #plot each column
    for i in range(size):
        plt.scatter(np.array(x_epics_sqr_arr_cropped[i]),x_contrasts_sqr_cropped[i],c=color[i])
    plt.scatter(x_epics_arr_average,x_contrasts_average,c='blue')

    p, c = np.polyfit(x_epics_arr_average, x_contrasts_average, 1, w=x_contrasts_stds, cov=True)
    e = np.sqrt(np.diag(c))
    #print([p,c,e])
    #print([p[0],e[0]])
    slope=sci_not(p[0],e[0])
    offset=sci_not(p[1],e[1])
    plt.plot(np.array(x_epics_arr_average),offset[0]*float(10)**offset[2]+np.array(x_epics_arr_average)*slope[0]*float(10)**slope[2])
    slope=sci_not(p[0],e[0],True)
    offset=sci_not(p[1],e[1],True)
    slope_str= '('+str(slope[0])+'\\pm'+str(slope[1])+')e'+str(slope[2]) if slope[2] != 0 else str(slope[0])+'\\pm'+str(slope[1])
    print('Gx: '+slope_str)
        #plt.scatter(np.array(x_epics_sqr_arr[i])-25.05,x_contrasts_sqr[i],c=color[i])
    plt.show()
