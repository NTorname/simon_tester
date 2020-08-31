# usage: sudo python3 REACTION.py [mac address] [# of samples] [file_name.csv]

from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep, clock_gettime, CLOCK_MONOTONIC
from threading import Event
import sys, random, csv, os

s1 = s2 = True
k = int(sys.argv[2])
data = []

#callback when gpio input state found
#this may be the most convoluted way to read a GPIO in the history of 
#computing and I'm not sure whose fault it is
def data_handler1(context, data):
	global s1
	s1 = bool(parse_value(data))
libmetawear.callback1 = FnVoid_VoidP_DataP(data_handler1)

def data_handler2(context, data):
	global s2
	s2 = bool(parse_value(data))
libmetawear.callback2 = FnVoid_VoidP_DataP(data_handler2)


#set up metatracker
device = MetaWear(sys.argv[1])
device.connect()
print("\nConnected")

libmetawear.mbl_mw_gpio_set_pull_mode(device.board, 0, 1) #0 = pull up
libmetawear.mbl_mw_gpio_set_pull_mode(device.board, 1, 1) #1 = pull down
libmetawear.mbl_mw_gpio_set_pull_mode(device.board, 2, 1) #2 = float
libmetawear.mbl_mw_gpio_set_pull_mode(device.board, 3, 1)
libmetawear.mbl_mw_gpio_set_pull_mode(device.board, 4, 0) 
libmetawear.mbl_mw_gpio_set_pull_mode(device.board, 5, 0)

libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 0) #good practice
libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 1) #cleans ungraceful shutdown
libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 2) 
libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 3) 
print("configured pins")


#subscribe to gpio inputs
signal1 = libmetawear.mbl_mw_gpio_get_digital_input_data_signal(device.board, 4)
libmetawear.mbl_mw_datasignal_subscribe(signal1, None, libmetawear.callback1)

signal2 = libmetawear.mbl_mw_gpio_get_digital_input_data_signal(device.board, 5)
libmetawear.mbl_mw_datasignal_subscribe(signal2, None, libmetawear.callback2)
print("subscribed listener\n")


#starting reaction testing
while k > 0:
	sleep(random.randrange(1,2)) #random delay vibration
	j = random.randrange(0,5) #select random motor
	print(j)

	if j == 4: #quick implementation of tricking user

		libmetawear.mbl_mw_gpio_set_digital_output(device.board, 0)
		libmetawear.mbl_mw_gpio_set_digital_output(device.board, 1)
		libmetawear.mbl_mw_gpio_set_digital_output(device.board, 2)
		libmetawear.mbl_mw_gpio_set_digital_output(device.board, 3)

		correct = True

		a = 0
		while(a < 200): #thats about two seconds
			libmetawear.mbl_mw_datasignal_read(signal1)
			sleep(0.004)
			libmetawear.mbl_mw_datasignal_read(signal2)
			sleep(0.004) #bad but polling too quick causes stability issues
			a += 1

			if (not(s1) or not(s2)):
				correct = False

		libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 0)
		libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 1)
		libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 2)
		libmetawear.mbl_mw_gpio_clear_digital_output(device.board, 3)

		print("%r reaction to trick" % (correct))
		data.append([j, correct, 999])
		k -= 1

	else:

		libmetawear.mbl_mw_gpio_set_digital_output(device.board, j)
		start = clock_gettime(CLOCK_MONOTONIC)

		while(s1 and s2): #wait for input
			libmetawear.mbl_mw_datasignal_read(signal1)
			sleep(0.004)
			libmetawear.mbl_mw_datasignal_read(signal2)
			sleep(0.004) #bad but polling too quick causes stability issues

		if j % 2: #determine if input was correct
			correct = not(s2)
		else:
			correct = not(s1)

		stop = clock_gettime(CLOCK_MONOTONIC)
		libmetawear.mbl_mw_gpio_clear_digital_output(device.board, j)
	
		while(not(s1 and s2)): #debouncing
			libmetawear.mbl_mw_datasignal_read(signal1)
			sleep(0.004)
			libmetawear.mbl_mw_datasignal_read(signal2)
			sleep(0.004)

		print("%r reaction to motor %d was %f seconds" % (correct, j, (stop - start)))
		data.append([j, correct, (stop-start)])
		k -= 1


#write results to file
with open(sys.argv[3], 'w') as reac_file:
	writer = csv.writer(reac_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['motor', 'correct button', 'reaction time (s)'])
	for a in data:
		writer.writerow([a[0], a[1], a[2]])

os.system("chmod 666 {}".format(sys.argv[3])) #metawear python only runs with sudo


#shut down
libmetawear.mbl_mw_datasignal_unsubscribe(signal1)
libmetawear.mbl_mw_datasignal_unsubscribe(signal2)
print("\nunsubscribed")
device.disconnect()
print("disconnected")
