import matplotlib.pyplot as plt
import scipy.stats
import numpy as np


x_min = 0.0
x_max = 2.0

mean = 1.0 
std2= 0.3
std3= 0.15
std4=0.1

x = np.linspace(x_min, x_max, 100)
y2 = scipy.stats.norm.pdf(x,mean,std2)
y3 = scipy.stats.norm.pdf(x,mean,std3)
y4 = scipy.stats.norm.pdf(x,mean,std4)

plt.plot(x,y2, color='blue', label="MPU-6050")
plt.plot(x,y3, color='green', label="PicoScopePP877")
plt.plot(x,y4, color='red', label="ADXL335")

plt.legend(loc="upper left")

plt.grid()

plt.xlim(x_min,x_max)

plt.title('Plot a Normal Distribution of Sensor',fontsize=10)

plt.xlabel('Accelerometer Position')
plt.ylabel('Normal Distribution')

plt.show()