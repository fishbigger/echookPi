"""
================================== 
BLUETOOTH DATA PACKETING FUNCTIONS
==================================
 * The two functions in this section handle packeting the data and sending it over USART to the bluetooth module. The two functions are
 *  identically named so are called the in the same way, however the first is run if the value passed to it is a float and the second is
 *  run if the value passed into it is an integer (an override function). For all intents and purposes you can ignore this and simply call
 *  'sendData(identifier, value);' using one of the defined identifiers and either a float or integer value to send informaion over BT.
 *
 * identifier:  see definitions at start of code
 * value:       the value to send (typically some caluclated value from a sensor)
"""

import random

def convertData(indentifier, value):
	value = float(value)
	if value == 0:
		#It is impossible to send null bytes over Serial connection
		#so instead we define zero as 0xFF or 11111111 i.e. 255
		dataByte1 = 0xFF
		dataByte2 = 0xFF

	elif value <= 127:
		#Values under 128 are sent as a float
		#i.e. value = dataByte1 + dataByte2 / 100

		integer = int(value)
		tempDecimal = (value - integer) * 100;
		decimal = int(tempDecimal)

		dataByte1 = integer
		dataByte2 = decimal

		if decimal == 0:
			dataByte2 = 0xFF

		if integer == 0:
			dataByte1 = 0xff

	else:
		#Values above 127 are sent as integer
		#i.e. value = dataByte1 * 100 + dataByte2

		hundreds = int(value / 100)
		tens = value - hundreds * 100

		dataByte1 = hundreds
		dataByte1 += 128

		dataByte2 = int(tens)

		if tens == 0:
			dataByte2 = 0xFF

		if hundreds == 0:
			dataByte1 = 0xFF

	dataByte1.to_bytes(1, "big")
	dataByte2.to_bytes(1, "big")

	return dataByte1, dataByte2

try:
	dataToSend = convertData("Vt", random.randint(0, 255))

	with open ('/dev/rfcomm0', 'w', 1) as f:
		f.write(dataToSend)

except:
	print ("Something went wrong")
