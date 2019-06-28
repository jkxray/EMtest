import numpy as np
from decimal import Decimal
import math

def myround(x, base):
    rounded=np.sign(x)*round(np.abs(x/base))*base
    return int(rounded)
def sci_not(value,uncertainty,Str=False):
    sigfig=10
    arg='%.'+str(sigfig)+'e'
    v=str(arg % Decimal(value)).split('e')
    u=str(arg % Decimal(uncertainty)).split('e')
    v[0]=float(v[0])
    u[0]=float(u[0])
    v[1]=int(v[1])
    u[1]=int(u[1])
    v.append(0)
    u.append(1)
    min=u
    max=v
    if v[1] < u[1]:
        min=v
        max=u
    mag=min[1]
    engi_mag = myround((min[1]+max[1])/2,3)
    mi = round(min[0])
    mx = round(max[0],np.abs(max[1]-min[1]))
    
    mi = round(mi*float(10)**(min[1]-engi_mag),np.abs(min[1]-engi_mag))
    mx = round(mx*float(10)**(max[1]-engi_mag),np.abs(min[1]-engi_mag))

    out=[mx,mi,engi_mag]
    if min[2]==0:
        out=[mi,mx,engi_mag]
    if Str==True:
        return ['%g'% out[0],'%g'% out[1],out[2]]
    return out