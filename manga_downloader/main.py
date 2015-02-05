#!/usr/bin/python

import libUrl, osFunc, prettyPrint, level
import re, sys

getUrl 			= libUrl.getUrl

mkdir 			= osFunc.mkdir
exist 			= osFunc.existFile
writeFile 		= osFunc.writeFile
appendFile 		= osFunc.appendFile
home_dir		= osFunc.getHomeDir()

numFormat 		= prettyPrint.num_format
logInfo			= prettyPrint.info
logError		= prettyPrint.error

repair			= level.straight_file
returnUrl		= level.returnUrl

if len(sys.argv) > 1:
	manga_name = sys.argv[1]
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

# Create root dir
if mkdir(rootDir):
	logInfo ("Created root directory")

# Create download dir
mkdir(downloadDir)

# Download manga list file
# if not getUrl(urlMaster+"/alphabetical", listFile):
# 	logError("Can't download manga list")
# 	exit(255)
# else:
# 	logInfo("Manga list downloaded")

# Get manga's url from manga's list file
manga_url = returnUrl(listFile, manga_name)
if manga_url is None:
	logError("Can't find manga " + manga_name)
	exit(0)

# Download manga's volume page
# if not getUrl(urlMaster + manga_url, volumePage):
# 	logError("Can't download "+manga_name+"'s volume page")
# 	exit(255)
# else:
# 	logInfo(manga_name+"'s volume page downloaded")

if mkdir(rootDir + "/" + volumeName):
	logInfo("Created \" " + rootDir + "/" + volumeName + "\" folder")
	for number in range(1, 10000):
		pageUrl = returnUrl(volumePage, manga_name + " " + str(number))
		if pageUrl is None:
			break
		else:
			print urlMaster + pageUrl
