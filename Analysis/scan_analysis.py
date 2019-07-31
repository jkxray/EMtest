import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys

def scan(path):
    step_size=0.005
    f = open(path+"/scan_"+str(step_size)+"mm_sum.csv","w")
    fpd = open(path+"/scan_"+str(step_size)+"mm_pd.csv","w")
    fA = open(path+"/scan_"+str(step_size)+"mm_A.csv","w")
    fB = open(path+"/scan_"+str(step_size)+"mm_B.csv","w")
    fC = open(path+"/scan_"+str(step_size)+"mm_C.csv","w")
    fD = open(path+"/scan_"+str(step_size)+"mm_D.csv","w")

    with open(path+'/scan_'+str(step_size)+'mm.csv','r') as csvfile:

        plots = csv.reader(csvfile, delimiter=',')
        i=0
        out=''
        outpd=''
        outA='' ; outB='' ; outC='' ; outD=''
        for row in plots:
            pd=float(row[3])
            A=float(row[4])/1e6
            B=float(row[5])/1e6
            C=float(row[6])/1e6
            D=float(row[7])/1e6
            sum=A+B+C+D
            if i>0:
                if i%401==0:
                    f.write(out+'\n')
                    out=''
                    fpd.write(outpd+'\n')
                    outpd=''
                    fA.write(outA+'\n')
                    outA=''
                    fB.write(outB+'\n')
                    outB=''
                    fC.write(outC+'\n')
                    outC=''
                    fD.write(outD+'\n')
                    outD=''
                else:
                    out+=str(sum)+', '
                    outpd+=str(pd)+', '
                    outA+=str(A)+', '
                    outB+=str(B)+', '
                    outC+=str(C)+', '
                    outD+=str(D)+', '
            i+=1
    fpd.close()
    f.close()
    fA.close()
    fB.close()
    fC.close()
    fD.close()
