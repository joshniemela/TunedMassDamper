"""
Collects data from 2 vl6180x sensors and stores it into a .csv file
"""
import time
import board
import busio
import adafruit_vl6180x as vlx
import pandas as pd

def changeAddress(before, after):
	"""
	Changes the I²C address of a vl6180x sensor.
	"""

	# Register address for the vl1680x sensor found at https://www.st.com/resource/en/datasheet/vl6180x.pdf
	I2C_SLAVE_DEVICE_ADDRESS = 0x212
	temp = vlx.VL6180X(i2c, address = before)
	temp._write_8(I2C_SLAVE_DEVICE_ADDRESS, after)


i2c = busio.I2C(board.SCL ,board.SDA)

input("Press enter to change the I²C address of the first sensor, make sure that only one sensor is connected")

# Change the I²C address of the first sensor to 0x28
changeAddress(0x29, 0x28)

input("Press enter to start collecting data, assure that both sensors are connected")

sensor1 = vlx.VL6180X(i2c, address = 0x29)
sensor2 = vlx.VL6180X(i2c, address = 0x28)

range_data1 = []
range_data2 = []
time_data = []
start_time = time.time()
while True:
	# Collect data from the sensors
	try:
		range1, range2 = sensor1.range, sensor2.range

		run_time = time.time()-start_time
		range1_data.append(range1)
		range1_data.append(range2)
		time_data.append(run_time)
		print(f"Range:{range1}mm, {range2}mm, Time: {run_time}")
		for sensor in [sensor1, sensor2]:
			if sensor.range_status != 0: print(f"Sensor {sensor.address} error: {sensor.range_status}")
		
	except KeyboardInterrupt:
		# Save the data into a .csv file
		zippedRanges = list(zip(range1_data, range2_data))
		df = pd.DataFrame(zippedRanges, columns=["sensor1[mm]", "sensor2[mm]"], index=time_data)
		df.index.name = "Time[s]"
		print("Done collecting")
		df.to_csv("data.csv")
		print(df)
		exit()
