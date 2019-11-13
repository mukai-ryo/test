#coding:utf-8

import numpy as np

signal_orig = [1,2]
signal_late = [0,1,2]

c = np.correlate(signal_late,signal_orig,"full")
ci = np.correlate(signal_orig,signal_late,"full")
print(c)
print(ci)
