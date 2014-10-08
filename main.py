#!/usr/bin/python

import LibUrl, re, datetime, os

urlMaster = "http://www.epocacosmeticos.com.br"
getUrl = LibUrl.getUrl

def prettyPrint(number):
	if number < 10:
		numStr = "0000"+str(number)
	elif number < 100:
		numStr = "000"+str(number)
	else:
		numStr = "00"+str(number)

	return numStr

def mkdir(dirName):
	valRet = None
	if not os.path.exists(dirName):
		os.makedirs(dirName)
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

def getSKU(fileName):
	for line in open(fileName, "r"):
		if "sku-ean-code" in line:
			sku = str(line.split(">")[1].split("<")[0])
			break

	return sku

def infoToCSV(fileName, stream):
	if not os.path.exists(fileName):
		writeFile(fileName, "\"HEAD\",\"PRODUCT\",\"URL\"\n")
		appendFile(fileName, stream)
	else:
		appendFile(fileName, stream)

lvlOneDir = "/tmp/lvl1"
print "["+str(datetime.datetime.now())+"][Level 1][INFO ] Fetching page with all brands"
if mkdir(lvlOneDir):
	url = urlMaster + "/marcas"
	urlListLvl1 = []
	if getUrl(url, lvlOneDir+"/brand.html"):
		fd2 = open(lvlOneDir+"/brand.html", "r")
		for line in fd2:
			if "BreadCrumb" in line:
				writeFile(lvlOneDir+"/brand.url.tmp", line.replace("><", ">\n<"))

		fd3 = open(lvlOneDir+"/brand.url.tmp", "r")
		for line in fd3:
			if "href" in line:
				keep1 = line
			if "src=\"/arquivos" in line:
				urlListLvl1.append("http://www.epocacosmeticos.com.br"+re.search('"(.*?)"', keep1.replace("\n", "")).group(0).replace("\"", ""))
			if "www.epocacosmeticos.com.br" in line and not "menu-item-texto" in line:
				urlListLvl1.append(re.search('"(.*?)"', line.replace("\n", "")).group(0).replace("\"", ""))
		fd3.close()

	urlListLvl1.sort()
	for url in urlListLvl1:
		appendFile(lvlOneDir+"/brand.url", url+"\n")

	del urlListLvl1

lvlTwoDir = "/tmp/lvl2"
mkdir(lvlTwoDir)
fileNumber = 0
print "["+str(datetime.datetime.now())+"][Level 2][INFO ] Fetching all brands' pages"
for url in open(lvlOneDir+"/brand.url", "r"):
	lvl2File = lvlTwoDir+"/"+str(fileNumber)+".html"
	lvl2FileNext = lvlTwoDir+"/"+str(fileNumber + 1)+".html"

	flag = 0
	beenHere = 0
	menu = ""

	if not os.path.exists(lvl2File):
		if getUrl(url, lvl2File):
			for line in open(lvl2File, "r"):
				if "search-single-navigator" in line:
					flag = 1
				if flag == 1 and ("<h3 class=" in line):
					menu = line.split("\"")[1]
				if flag == 1 and "<ul class=\""+menu.lower()+"\">" in line.lower():
					flag = 2
				if flag == 2 and "<a href" in line:
					appendFile(lvlTwoDir+"/brands.url", line.split("\"")[1]+"\n")
					print "["+str(datetime.datetime.now())+"][Level 2]["+prettyPrint(fileNumber)+"] "+line.split("\"")[1]
					beenHere = 1
				if flag == 2 and "</ul>" in line:
					flag = 1
			if beenHere == 0:
				print "["+str(datetime.datetime.now())+"][Level 2][ERROR] Not a brand page: "+url.replace("\n","")
				appendFile(lvlTwoDir+"/errors.url", url)
		else:
			print "["+str(datetime.datetime.now())+"][Level 2][ERROR] Can't get "+url.replace("\n","")
			appendFile(lvlTwoDir+"/errors.url", url)
	fileNumber += 1

if os.path.exists(lvlTwoDir+"/errors.url"):
	fileNumber = 0
	for url in open(lvlTwoDir+"/errors.url", "r"):
		if getUrl(url, lvlTwoDir+"/"+str(fileNumber)+"-retry.html"):
			for line in open(lvlTwoDir+"/"+str(fileNumber)+"-retry.html", "r"):
				if "search-single-navigator" in line:
					flag = 1
				if ((flag == 1) and ("?PS=20" in line) and ("<a href" in line)):
					print "["+str(datetime.datetime.now())+"][Level 2]["+prettyPrint(fileNumber)+"][Retrying] "+ line.replace("\n", "").split("\"")[1]
					appendFile(lvlTwoDir+"/brands.url", line.split("\"")[1]+"\n")
		fileNumber += 1
	os.remove(lvlTwoDir+"/errors.url")

lvlThreeDir = "/tmp/lvl3"
mkdir(lvlThreeDir)
fileNumber = 0
print "["+str(datetime.datetime.now())+"][Level 3][INFO ] Getting information about the product"
for line in open(lvlTwoDir+"/brands.url", "r"):
	if getUrl(line, lvlThreeDir+"/"+str(fileNumber)+"-brandPage.html"):
		head = ""
		for line in open(lvlThreeDir+"/"+str(fileNumber)+"-brandPage.html"	, "r"):
			product = ""
			productUrl = ""
			sku = ""
			flag = 0

			if "<title>" in line:
				head = line.split("<title>")[1].split("<")[0]

			if "<h3><a title=" in line:
				product = str(line.split("\"")[1])
				productUrl = str(line.split("\"")[3])
				if getUrl(productUrl, lvlThreeDir+"/"+str(fileNumber)+"-productPage.html"):
					sku = getSKU(lvlThreeDir+"/"+str(fileNumber)+"-productPage.html")
					if os.path.exists(lvlThreeDir+"/list.sku"):
						for skuLine in open(lvlThreeDir+"/list.sku", "r"):
							if sku in skuLine:
								flag = 1
					else:
						writeFile(lvlThreeDir+"/list.sku", sku)

					if flag == 0:
						print "["+str(datetime.datetime.now())+"][Level 3]["+prettyPrint(fileNumber)+"] ############################"
						print "["+str(datetime.datetime.now())+"][Level 3]["+prettyPrint(fileNumber)+"] "+head
						print "["+str(datetime.datetime.now())+"][Level 3]["+prettyPrint(fileNumber)+"] "+product
						print "["+str(datetime.datetime.now())+"][Level 3]["+prettyPrint(fileNumber)+"] "+productUrl

						getUrl(productUrl, lvlThreeDir+"/"+str(fileNumber)+"-productPage.html")
						appendFile(lvlThreeDir+"/list.sku", sku)
						infoToCSV(lvlThreeDir+"/productsList.csv", "\""+head+"\",\""+product+"\",\""+productUrl+"\"\n")
					else:
						print "["+str(datetime.datetime.now())+"][Level 3][ERROR] @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
						print "["+str(datetime.datetime.now())+"][Level 3][ERROR] SKU already registered: " + sku
					break
		fileNumber += 1
