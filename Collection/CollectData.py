from ophyd import EpicsSignal
import numpy as np
import time
from decimal import Decimal
import os
import sys
import threading
sys.path.append('../')
from Prologix import Prologix


from Configuration import *
import CollectDAC
import Calibrate
import CollectBias
import CollectCurrent
if data == 'calibrate':
    Calibrate.calibrate()
if data == 'bias':
    CollectBias.bias()

if data == 'dac':
    CollectDAC.dac()

if data == 'current':
    CollectCurrent.current()

if data == 'drift':
    print("Not supported.")
