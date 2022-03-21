import matplotlib.pyplot as plt
import scipy.stats
import numpy as np


x_min = 0.0
x_max = 16.0

mean = 8.0 
std1 = 0.11
std2= 0.3
std3= 0.15
std4=0.1

x = np.linspace(x_min, x_max, 100)
y1 = scipy.stats.norm.pdf(x,mean,std1)
y2 = scipy.stats.norm.pdf(x,mean,std2)
y3 = scipy.stats.norm.pdf(x,mean,std3)
y4 = scipy.stats.norm.pdf(x,mean,std4)

plt.plot(x,y1, color='coral', label="Flex Resistor")
plt.plot(x,y2, color='blue', label="MPU-6050")
plt.plot(x,y3, color='green', label="PicoScope")
plt.plot(x,y4, color='red', label="ADXL335")

plt.legend(loc="upper left")

plt.grid()

plt.xlim(x_min,x_max)

plt.title('Plot a normal distribution of Sensor 1',fontsize=10)

plt.xlabel('x')
plt.ylabel('Normal Distribution')

plt.show()