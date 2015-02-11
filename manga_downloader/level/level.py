#!/usr/bin/python

def returnUrl(file_name, manga_name):
	base_url = None

	fp = open(file_name, "r")
	for line in fp:
		if (">"+manga_name+"<" in line) or ("> "+manga_name+"<" in line) or (">"+manga_name+" <" in line):
			if "<a href=\"" in line:
				base_url = line.split("\"")[1]

	return base_url

def returnImageUrl(file_name):
	image_url = None

	fp = open(file_name, "r")
	for line in fp:
		if ("<img id=\"img\" width=\"" in line) and (" src=\"" in line) and (" name=\"img\" />" in line):
			image_url = line.split("src=")[1].split("\"")[1]

	return image_url

def returnPageUrl(file_name, number):
	page_url = None

	fp = open(file_name, "r")
	for line in fp:
		if ("option" in line) and (">"+str(number)+"<" in line):
			page_url = line.split("value=")[1].split("\"")[1]

	return page_url