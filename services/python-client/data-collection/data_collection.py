import serial
import csv
from datetime import datetime

# declare serial communication variables and file paths
serial_port = 'COM3' # com port
baud_rate = 57600
currentTime = str(datetime.now())
currentTime = currentTime.replace(':', '_')
pathRunningCsv = "%s_running.csv" % currentTime
ser = serial.Serial(serial_port, baud_rate) 
