import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,10]
import csv
from decimal import Decimal
import math
from format import sci_not
import sys
data='none'
path = '../data'
ave_time='1'
num_points=15
show_plot='y'
save_plot='n'
def main():
    for arg in sys.argv:
        if arg.split('=')[0]=='path':
            path=arg.split('=')[1]
        if arg.split('=')[0]=='averaging_time':
            ave_time=arg.split('=')[1]
        if arg.split('=')[0]=='data':
            data=arg.split('=')[1]
        if arg.split('=')[0]=='show_plot':
            show_plot=arg.split('=')[1]
        if arg.split('=')[0]=='save_plot':
            save_plot=arg.split('=')[1]
