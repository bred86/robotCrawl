#!/usr/bin/python

import datetime

def num_format (number):
	numStr = ""

	if number < 10:
		numStr = "00"+str(number)
	elif number < 100:
		numStr = "0"+str(number)

	return numStr

def log (string):
	print "["+str(datetime.datetime.now().strftime("%F %T"))+"]"+str(string)

def info (string):
	log(str("[INFO ] ") + string)

def error (string):
	log(str("[ERROR] ") + string)

def warn (string):
	log(str("[WARN ] ") + string)