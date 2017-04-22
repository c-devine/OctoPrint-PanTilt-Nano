#!/usr/bin/env python2

import sys
import argparse
import serial

port = '/dev/ttyUSB0'
baud = 9600


def main():
	parser = argparse.ArgumentParser(description='Command parser for nano.')
	parser.add_argument('pan', type=int, nargs='?', help='pan value')
	parser.add_argument('tilt', type=int, nargs='?', help='tilt value')
	parser.add_argument('--reset', action='store_true', help='reset all parmameters to default values')
	parser.add_argument('--config', dest="config", nargs=4, help='<panMin> <panMax> <tiltMin> <tiltMax>')
	args = parser.parse_args()

	print(vars(args))

	ser = serial.Serial()
	ser.baudrate = baud
	ser.port = port
	ser.setDTR(True)

	ser.open()
	ser.write('test\n')

	print(ser)
	ser.close()



if __name__ == "__main__":
	main()
