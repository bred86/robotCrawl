#!/usr/bin/python

import fileinput

def straight_file(file_name, searchStr, replaceStr):
	for line in fileinput.input(file_name, inplace=True):
		line.replace(searchStr, replaceStr)

def returnUrl(file_name, manga_name):
	base_url = None

	fp = open(file_name, "r")
	for line in fp:
		if (">"+manga_name+"<" in line) or ("> "+manga_name+"<" in line) or (">"+manga_name+" <" in line):
			if "<a href=\"" in line:
				base_url = line.split("\"")[1]

	return base_url