import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys

def scan(path,axis):
    i=0
    x=0
    y=-1
    out=''
    size=401
    fluxrr_pd=[]
    sensrr_d=[]

    epics_arr=[]
    Gs=[]
    contrasts=[]

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

            #calculate the flux from the photodiode
            flux_pd=pd*1e9/266.4e-9
            #append the flux measurement got from a pixel and append to a list
            fluxrr_pd.append(flux_pd)
            #calculate the sensitivity of diamond detector
            sens_d=0.99122*sum*266.4e-9/pd
            #append value to list
            sensrr_d.append(sens_d)

            #append all position data into a list and calculate the contrasts at each pixel
            if axis=='z':
                epics_arr.append(z_epics)
                G=(z_epics)*sum/((C+D)-(A+B))
                Gs.append(G)
                contrasts.append( ((C+D)-(A+B)) / (A+B+C+D) )
            elif axis=='x':
                epics_arr.append(x_epics)
                G=(x_epics)*sum/((A+D)-(B+C))
                Gs.append(G)
                contrasts.append(((A+D)-(B+C))/sum)

            i+=1

    #calculate the mean flux from photodiode and sensitivty of diamond
    flux_pd=np.mean(fluxrr_pd)
    sens_d=np.mean(sensrr_d)
    #print them out
    print('pd flux: '+str(flux_pd)+' +/- '+str(np.std(fluxrr_pd)/(len(fluxrr_pd)**0.5)))
    print('diamond sensitivity: '+str(sens_d)+' +/- '+str(np.std(sensrr_d)/(len(sensrr_d)**0.5)))

    epics_sqr_arr=[]
    contrasts_sqr=[]

    #slice 1 dimensional array into 2 dimensional array by rows
    for i in range(size):
        epics_sqr_arr.append(epics_arr[i*size:(i+1)*size])
        contrasts_sqr.append(contrasts[i*size:(i+1)*size])

    if axis=='z':
        #rotate matrix so it's sliced by columns
        epics_sqr_arr=np.rot90(epics_sqr_arr)
        contrasts_sqr=np.rot90(contrasts_sqr)
    #no need to do this for the x arrays because it's already sliced by rows which is what we want


    epics_sqr_arr_cropped=[]
    contrasts_sqr_cropped=[]

    #set offset for every column
    limits=0.5
    for i in range(size):
        offset=0
        for j in range(size):
            if contrasts_sqr[i][j] < limits and contrasts_sqr[i][j] > -1*limits:

                offset=epics_sqr_arr[i][j]+0.003
                #print(offset)
                break
        epics_sqr_arr[i]=np.array(epics_sqr_arr[i])-offset


    #crop z data and align
    for i in range(len(epics_sqr_arr)):
        epics_sqr_arr_cropped.append([])
        contrasts_sqr_cropped.append([])
        count=0
        for j in range(len(epics_sqr_arr[i])):
            #lim=0.1001
            lim=0.1001
            if epics_sqr_arr[i][j]>-1*lim and epics_sqr_arr[i][j]<1*lim:
                epics_sqr_arr_cropped[i].append(epics_sqr_arr[i][j])
                contrasts_sqr_cropped[i].append(contrasts_sqr[i][j])
        epics_sqr_arr_cropped[i]=np.array(epics_sqr_arr_cropped[i])
        contrasts_sqr[i]=np.array(contrasts_sqr[i])


    epics_arr_average=[]
    contrasts_average=[]
    contrasts_stds=[]
    #create 1 dimensional array of each row averaged
    epics_sqr_arr_cropped_temp=np.rot90(epics_sqr_arr_cropped,3)
    contrasts_sqr_cropped_temp=np.rot90(contrasts_sqr_cropped,3)
    for i in range(len(epics_sqr_arr_cropped_temp)):
        limits=0.015
        if np.median(epics_sqr_arr_cropped_temp[i])>=-1*limits and np.median(epics_sqr_arr_cropped_temp[i])<=limits:
            epics_arr_average.append(np.median(epics_sqr_arr_cropped_temp[i]))
            contrasts_average.append(np.mean(contrasts_sqr_cropped_temp[i]))

            contrasts_stds.append(np.std(contrasts_sqr_cropped_temp[i]))
    #create color gradient
    color=[]
    half = int(size/2)
    for i in range(half):
        color.append((i/half,0,50/255,0.1))
    for i in range(size-half):
        color.append((1,float(i)/(size-half),50/255,0.1))


    #plot each column
    for i in range(size):
        plt.scatter(np.array(epics_sqr_arr_cropped[i]),contrasts_sqr_cropped[i],c=color[i])
    plt.scatter(epics_arr_average,contrasts_average,c='blue')

    p, c = np.polyfit(epics_arr_average, contrasts_average, 1, w=contrasts_stds, cov=True)
    e = np.sqrt(np.diag(c))
    #print([p,c,e])
    #print([p[0],e[0]])

    slope=sci_not(p[0],e[0],True)
    offset=sci_not(p[1],e[1],True)
    slope_str= '('+str(slope[0])+'+/-'+str(slope[1])+')e'+str(slope[2]) if slope[2] != 0 else str(slope[0])+'+/-'+str(slope[1])


    slope=sci_not(p[0],e[0])
    offset=sci_not(p[1],e[1])
    plt.plot(np.array(epics_arr_average),offset[0]*float(10)**offset[2]+np.array(epics_arr_average)*slope[0]*float(10)**slope[2],label='Gz: '+slope_str)
        #plt.scatter(np.array(x_epics_sqr_arr[i])-25.05,x_contrasts_sqr[i],c=color[i])
    labels=None
    if axis=='z':
        labels=('Gz','Z')
    elif axis=='x':
        labels=('Gx','X')
    print(labels[0]+': '+slope_str)
    plt.xlabel(labels[1]+" position (mm)")
    plt.ylabel(labels[1]+" contrast")
    plt.legend()
    plt.show()
