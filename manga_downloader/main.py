#!/usr/bin/python

import libUrl, osFunc, prettyPrint, level
import re, sys

getUrl 			= libUrl.getUrl

mkdir 			= osFunc.mkdir
exist 			= osFunc.existFile
writeFile 		= osFunc.writeFile
appendFile 		= osFunc.appendFile
home_dir		= osFunc.getHomeDir()
getFileSize		= osFunc.getFileSize
getLastFile		= osFunc.getLastFile
getLastFolder	= osFunc.getLastFolder

numFormat 		= prettyPrint.num_format
logInfo			= prettyPrint.info
logWarn			= prettyPrint.warn
logError		= prettyPrint.error

returnUrl		= level.returnUrl
returnImageUrl	= level.returnImageUrl
returnPageUrl	= level.returnPageUrl

if len(sys.argv) > 1:
	manga_name 	= sys.argv[1].lower()
else:
	logError("Usage: "+ sys.argv[0] + " manga_name")
	exit(255)

volumeName		= manga_name.replace(" ","_").replace("/","_").replace("#","").replace("+","")
urlMaster 		= "http://www.mangareader.net"
rootDir			= home_dir + "/Imagens/Manga"
downloadDir		= rootDir + "/.download"
listFile		= downloadDir + "/list.html"
mangaList		= downloadDir + "/manga.list"
volumePage		= downloadDir + "/"+ volumeName + ".html"
volumeDir		= rootDir + "/" + volumeName
volumeDownload	= downloadDir+"/"+volumeName

# Create root dir
if mkdir(rootDir):
	logInfo ("Created root directory")

# Create download dir
mkdir(downloadDir)

# Download manga list file
if not getUrl(urlMaster+"/alphabetical", listFile):
	logError("Can't download manga list")
	exit(255)
else:
	logInfo("Manga list downloaded")

# Get manga's url from manga's list file
manga_url = returnUrl(listFile, manga_name)
if manga_url is None:
	logError("Can't find manga " + manga_name)
	exit(0)

# Download manga's volume page
if not getUrl(urlMaster + manga_url, volumePage):
	logError("Can't download "+manga_name+"'s volume page")
	exit(255)
else:
	logInfo(manga_name+"'s volume page downloaded")
	logInfo(volumeDir)

if mkdir(volumeDir):
	logInfo("Created \" " + volumeDir + "\" folder")

	folder = "0001-0100"
	mkdir(volumeDir+"/"+folder)
	for number in range(1, 10000):
		if ((number-1)%100 == 0) and (number >= 1):
			folder = numFormat(number)+"-"+numFormat(number + 99)
			mkdir(volumeDir+"/"+folder)
		
		# Grabbing the next page image's url
		for page in range(1, 1001):
			retry_next = 1

			if page == 1:
				pageUrl = returnUrl(volumePage, manga_name + " " + str(number))
				if pageUrl is None:
					break

				if not getUrl(urlMaster+pageUrl, volumeDownload+"_"+numFormat(number)+"_0001.html"):
					logWarn("Retryin for "+manga_name+" "+numFormat(number)+"["+numFormat(retry_next)+"/5 ]")
					if retry_next <= 5:
						number 	-= 1
						retry_next 	+= 1
						continue
				else:
					logInfo(manga_name+" "+numFormat(number)+" / 0001")

			pageUrl = returnPageUrl(volumeDownload+"_"+numFormat(number)+"_"+numFormat(page)+".html", (page + 1))
			if pageUrl is None:
				break

			if not getUrl(urlMaster+pageUrl, volumeDownload+"_"+numFormat(number)+"_"+numFormat(page + 1)+".html")[0]:
				logWarn("Retryin for "+manga_name+" "+numFormat(number)+"["+numFormat(retry_next)+"/5 ]")
				if retry_next <= 5:
					page 	-= 1
					retry_next 	+= 1
					continue
			else:
				logInfo(manga_name+" "+numFormat(number)+" / "+numFormat((page + 1)))

			image_size_header 	= 1
			image_size_file 	= 0
			while (int(image_size_header) > int(image_size_file)):
				ret_val, image_size_header = getUrl(returnImageUrl(volumeDownload+"_"+numFormat(number)+"_"+numFormat(page + 1)+".html"), volumeDir+"/"+folder+"/cap_"+numFormat(number)+"_"+numFormat(page + 1)+".jpeg")
				if ret_val:
					image_size_file = getFileSize(volumeDir+"/"+folder+"/cap_"+numFormat(number)+"_"+numFormat(page + 1)+".jpeg")
				else:
					image_size_header 	= 1
					image_size_file 	= 0
else:
	flag = 0
	last_dir = getLastFile(rootDir + "/" + volumeName)
	last_file = getLastFile(rootDir + "/" + volumeName + "/" + last_dir)

	logInfo("\"" + volumeDir + "\" already exists. Continuing from file " + last_dir + "/" + last_file)

	for number in range(int(last_file.split("_")[1]), 10000):
		folder = getLastFolder(volumeDir)

		if ((number-1)%100 == 0) and (number >= 1):
			folder = numFormat(number)+"-"+numFormat(number + 99)
			mkdir(volumeDir+"/"+folder)
		page = 0
		
		while page <= 1000:
			retry_next = 1

			if (number == int(last_file.split("_")[1])) and (flag == 0):
				page = int(last_file.split("_")[2].split(".")[0])
				flag = 1

			pageUrl = returnUrl(volumePage, manga_name + " " + str(number))
			if pageUrl is None:
				break

			if page < 10:
				pagehtml = "000"+str(page)
			elif page < 100:
				pagehtml = "00"+str(page)
			elif page < 1000:
				pagehtml = "0"+str(page)
			else:
				pagehtml = str(page)

			if not getUrl(urlMaster+pageUrl, volumeDownload+"_"+numFormat(number)+"_"+pagehtml+".html")[0]:
				logWarn("Retryin for "+manga_name+" "+numFormat(number)+"["+numFormat(retry_next)+"/5 ]")
				if retry_next <= 5:
					number 	-= 1
					retry_next 	+= 1
					continue

			pageUrl = returnPageUrl(volumeDownload+"_"+numFormat(number)+"_"+numFormat(page)+".html", (page + 1))
			if pageUrl is None:
				break

			if not getUrl(urlMaster+pageUrl, volumeDownload+"_"+numFormat(number)+"_"+numFormat(page + 1)+".html"):
				logWarn("Retryin for "+manga_name+" "+numFormat(number)+"["+numFormat(retry_next)+"/5 ]")
				if retry_next <= 5:
					page 	-= 1
					retry_next 	+= 1
					continue
			else:
				logInfo(manga_name+" "+numFormat(number)+" / "+numFormat((page + 1)))

			image_size_header 	= 1
			image_size_file 	= 0
			while (int(image_size_header) > int(image_size_file)):
				ret_val, image_size_header = getUrl(returnImageUrl(volumeDownload+"_"+numFormat(number)+"_"+numFormat(page + 1)+".html"), volumeDir+"/"+folder+"/cap_"+numFormat(number)+"_"+numFormat(page + 1)+".jpeg")
				if ret_val:
					image_size_file = getFileSize(volumeDir+"/"+folder+"/cap_"+numFormat(number)+"_"+numFormat(page + 1)+".jpeg")
				else:
					image_size_header 	= 1
					image_size_file 	= 0
			page += 1
