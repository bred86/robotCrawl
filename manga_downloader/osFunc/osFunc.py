#!/usr/bin/python

import os

def mkdir(dirName):
	valRet = False
	if not os.path.exists(dirName):
		os.makedirs(dirName)
		valRet = True
	
	return valRet

def existFile(fileName):
	valRet = False
	if os.path.isfile(fileName):
		valRet = True

	return valRet

def writeFile(fileName, stream):
	fd = open(fileName, "w")
	fd.write(stream)
	fd.close()

def appendFile(fileName, stream):
	fd = open(fileName, "a")
	fd.write(stream)
	fd.close()

def getHomeDir():
	return os.path.expanduser("~")

def getFileSize(file_name):
	return os.stat(file_name).st_size