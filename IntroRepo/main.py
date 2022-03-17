# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from math import sqrt, floor, ceil
import numpy as np
import matplotlib.pyplot as plt

def sample(max, min,numberofsteps,time):
    slope = (max-min)/numberofsteps
    ans = slope*time
    return ans

def pointslopeform(x1,y1,x2,y2):
    m = (y2-y1)/(x2-x1)
    b = (y1-m*x1)
    return m,b

def sawtoothwave_eq(wavelength, max, min, x_0, time):
    #initializing variables
    cycles = 0
    locationalongwave = time
    while cycles <= time/wavelength:
        cycles = cycles + 1
  #      print("cycles", cycles)
    if cycles > 1:
        locationalongwave = time - wavelength*(cycles-1)


 #   print("wavetime =", wavetime)
    if locationalongwave<=(0.5*wavelength):
        going = True
    else:
        going = False
#    print("going =",going)
    if going:
        [m, b] = pointslopeform(x_0, min, x_0+wavelength/2, max)
        #print("First Equation", m, b)
    else:
        [m, b] = pointslopeform(x_0 + wavelength/2, max, x_0+wavelength, min)
       # print("Second Equation", m, b)
    YValue = m*locationalongwave+b
    return YValue


print("Valve Position", sawtoothwave_eq(200, 100, 0, 0, 200))

# time = np.linspace(0,200,3000)
# i = 0
# wavevalue = np.linspace(0,len(time),3000)
# for value in time:
#     wavevalue[i] = sawtoothwave_eq(50,30,0,0,value)
#     i = i+1
#
# plt.plot(time,wavevalue,time,np.ones(len(time))*30,time,np.ones(len(time))*0)
# plt.show()

#####################
#
# def trigger(dwelltime, numberofstep, cycles, t_0, time):
#
#     triggered = 1
#     return triggered
#
#
# time = np.linspace(0,4000,30000)
# i = 0
# triggered_value = np.linspace(0,len(time),30000)
# for value in time:
#     triggered_value[i] = trigger(20,5,3,0,value)
#     i = i+1
#
# plt.plot(time,triggered_value)
# plt.show()

datax = ("mia","fred","fredrick","pashton","frilda","greg","francis")
datay = (40,34,56,18,23,43)



