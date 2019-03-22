
# pr_curve.py
# coding:utf-8
 
import numpy as np
import matplotlib.pyplot as plt
 
#data=np.loadtxt('pr.txt')
#mean=np.mean(data[:,1:],axis=1)
tick=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
carData = [0, 0.5286, 0.853047, 0.985782, 0.989796, 0.993333, 0.993333, 1, 1 ,1, 1]
truckData = [0, 0.210614, 0.735484, 0.847458, 0.928571, 0.948052, 0.948052, 0.977778, 1, 1, 1]
personData = [0, 0, 0.0190311, 0.0326364, 0.0450205, 0.0860013 ,0.410448, 0.466292, 0.610526, 0.777778, 1]
bicycleData = [0, 0, 0, 0, 0, 0 ,0,0, 0, 0, 0]
busData = [0, 0, 0, 0.161137, 0.4, 0.857143, 0.857143, 0.857143, 0.857143, 0.857143, 0.857143]
motorbikeData = [0, 0, 0, 0, 0, 0 ,0,0, 0, 0, 0]
dangerouscarData = [0, 0, 0, 0, 0, 0 ,0,0, 0, 0, 0]


fig = plt.figure()
plt.subplot(3,3,1)
plt.title('car, MAP=0.849445')
#plt.xlabel('Recall')
#plt.ylabel('Precision')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick,carData[::-1])
 
plt.subplot(3,3,2)
plt.title('truck, MAP=0.781455')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick,truckData[::-1])
 
plt.subplot(3,3,3)
plt.title('Person, MAP=0.31343')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick,personData[::-1])
 
plt.subplot(3,3,4)
plt.title('bicycle, MAP=0, Missing label')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick,bicycleData[::-1])

plt.subplot(3,3,5)
plt.title('bus, MAP=0.531532')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick, busData[::-1])

plt.subplot(3,3,6)
plt.title('motorbike, MAP=0.19584')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick,motorbikeData[::-1])

plt.subplot(3,3,7)
plt.title('dangerouscar, MAP=0')
plt.axis([0, 1, 0, 1.05])
plt.xticks(tick)
plt.yticks(tick)
plt.plot(tick,dangerouscarData[::-1])

plt.show()
fig.tight_layout()