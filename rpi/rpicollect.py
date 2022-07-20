"""
Collects data from 2 vl6180x sensors and stores it into a .csv file
"""
import time
import board
import busio
import adafruit_vl6180x
import numpy as np
import pandas as pd
i2c = busio.I2C(board.SCL ,board.SDA)

sensor1 = adafruit_vl6180x.VL6180X(i2c, address = 0x29)
sensor2 = adafruit_vl6180x.VL6180X(i2c, address = 0x28)

range_data1 = []
range_data2 = []
time_data = []
start_time = time.time()
while True:
	try:
		range1 = sensor1.range
		status1 = sensor1.range_status

		range2 = sensor2.range
		status2 = sensor2.range_status

		run_time = time.time()-start_time
		range_data1.append(range1)
		range_data2.append(range2)
		time_data.append(run_time)
		print(f"Range:{range1}mm, {range2}mm, Time: {run_time}")
		if status1 != 0:
			print(status1)
	except KeyboardInterrupt:
		zipped = list(zip(range_data1, range_data2))
		df = pd.DataFrame(zipped, columns=["sensor1[mm]", "sensor2[mm]"], index=time_data)
		df.index.name = "Time[s]"
		print("Done collecting")
		df.to_csv("data.csv")
		print(df)
		exit()
