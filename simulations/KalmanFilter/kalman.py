from matplotlib.animation import FuncAnimation
import numpy as np
import csv
import matplotlib.pyplot as plt
import time
import random

"""
Kalman Filter for Accelertometer noise reduction

Algorithm
1. Inialize variables and constants 
    - Choose process variance constant (Q), and measurement constant (R) using raw data
    - Estimated state variable (x_t) = 0; State variance variable (P_t) = 1
2. Set input of Kalman filter to unprocessed sensor data
3. Calculate Prediction Params
    - prediction estimated state variable (xt_predict)
    - prediction state variance variable (Pt_predict)
4. Calculate Update Prams
    - Kalman gain (K_t)
    - updated estimated state variable (x_t) - this is the filtered data i.e. output
    - updated state variance variable (P_t)
"""

class KalmanFilter():
    def __init__(self):
        #Initialize values
        self.Q = 0.1
        self.R = 50
        self.Pt_previous = 1
        self.xt_previous = 1        #use mean as initial previous val

        self.KalmanOutput = 0

        self.raw_data_array = []
        self.kalman_filtered_array = []
        self.x_axis = []

        self.start_plotting()
    
    def start_plotting(self):
        self.ani = FuncAnimation(plt.gcf(), self.kalman, interval=100)
        plt.show()

    def kalman(self, i):
        mean = 1
        std_dev = 0.5
        self.raw_data = np.random.normal(mean, std_dev)        #adjust for appropriate variance; here is +/- 0.5 from mean
        #self.raw_data = np.random.poisson(mean)
        #self.raw_data = np.random.rayleigh(mean)
        self.xt_update = self.xt_previous
        self.Pt_update = self.Pt_previous + self.Q
        self.K_t = self.Pt_update / (self.Pt_update + self.R)
        self.x_t = self.xt_update + (self.K_t * (self.raw_data - self.xt_update))
        self.P_t = (1 - self.K_t) * self.Pt_update
        self.xt_previous = self.x_t
        self.pt_previous = self.P_t

        self.KalmanOutput = self.x_t

        self.raw_data_array.append(self.raw_data)
        self.kalman_filtered_array.append(self.KalmanOutput)
        self.x_axis.append(time.time()) 

        plt.cla()
        plt.plot(self.x_axis, self.raw_data_array, label="Raw Data")
        plt.plot(self.x_axis, self.kalman_filtered_array, label="Kalman Filtered")
        plt.legend(loc="upper right")

        plt.xlabel('UNIX Time')
        plt.ylabel('Acceleration')
        plt.title('Raw acceleration data comparison with Kalman filtered output')
        plt.grid(True)

if __name__ == "__main__":
    k = KalmanFilter()
