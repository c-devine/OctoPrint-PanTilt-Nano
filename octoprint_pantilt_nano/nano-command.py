#!/usr/bin/env python2
from __future__ import absolute_import
import sys
import json
import argparse
import serial
import time

port = '/dev/ttyUSB0'
baud = 9600


def main():
	parser = argparse.ArgumentParser(description='Command parser for nano.')
	parser.add_argument('--pan', type=int, help='pan value')
	parser.add_argument('--tilt', type=int, help='tilt value')
	parser.add_argument('--reset', action='store_true', help='reset all parmameters to default values')
	parser.add_argument('--exit', action='store_true', help='exit')
	parser.add_argument('--print_settings', action='store_true', help='print settings')
	parser.add_argument('--config', type=int, nargs=4, help='<panMin> <panMax> <tiltMin> <tiltMax>')

	ser = serial.Serial(timeout=1)
	ser.baudrate = baud
	ser.port = port

	try:
		ser.open()
		ser.setDTR(level=False)
	except Exception as e:
		print('Error opening {} : {}'.format(port, e))
		exit(1);

	while (True):
		command = raw_input('>')
		try:
			args = parser.parse_args(command.split())
			#print(args)
			if (args.exit):
				break
			if (args.reset):
				ser.write("{command:'reset'}\n")
				print(ser.readline())
			if (args.print_settings):
				ser.write("{command:'print_settings'}\n")
				print(ser.readline())
			if (args.config is not None):
				ser.write("{{command:'set', target:'panMin', value:{}}}\n".format(args.config[0]))
				print(ser.readline())
				ser.write("{{command:'set', target:'panMax', value:{}}}\n".format(args.config[1]))
				print(ser.readline())
				ser.write("{{command:'set', target:'tiltMin', value:{}}}\n".format(args.config[2]))
				print(ser.readline())
				ser.write("{{command:'set', target:'tiltMax', value:{}}}\n".format(args.config[3]))
				print(ser.readline())
			if (args.pan is not None):
				ser.write("{{command:'set', target:'panUs', value:{}}}\n".format(args.pan))
				print(ser.readline())
			if (args.tilt is not None):
				ser.write("{{command:'set', target:'tiltUs', value:{}}}\n".format(args.tilt))
				print(ser.readline())

		except Exception, e:
			print(e.message)
		except SystemExit, ex:
			pass

	ser.close()
	exit(0)


if __name__ == "__main__":
	main()
