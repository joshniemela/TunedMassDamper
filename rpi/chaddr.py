    """
    Small script used to change the I²C address of a vl6180x sensor.
    """
import busio
import board
import adafruit_vl6180x

i2c = busio.I2C(board.SCL, board.SDA)
temp = adafruit_vl6180x.VL6180X(i2c, address = 0x29)
temp._write_8(0x212, 0x28)
