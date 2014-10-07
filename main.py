#!/usr/bin/python

import LibUrl, re

urlMaster = "http://www.epocacosmeticos.com.br"
urlListLvl1 = []

getUrl = LibUrl.getUrl

url = urlMaster + "/marcas"
print "LVL 1"
if getUrl(url, "/tmp/lvl1.tmp"):
	fd2 = open("/tmp/lvl1.tmp", "r")
	for line in fd2:
		if "BreadCrumb" in line:
			fd3 = open("/tmp/lvl1_urls.tmp", "w")
			fd3.write(line.replace("><", ">\n<"))
			fd3.close()

	fd3 = open("/tmp/lvl1_urls.tmp", "r")
	for line in fd3:
		if "href" in line:
			keep1 = line
		if "src=\"/arquivos" in line:
			urlListLvl1.append("http://www.epocacosmeticos.com.br"+re.search('"(.*?)"', keep1.replace("\n", "")).group(0).replace("\"", ""))
		if "www.epocacosmeticos.com.br" in line and not "menu-item-texto" in line:
			urlListLvl1.append(re.search('"(.*?)"', line.replace("\n", "")).group(0).replace("\"", ""))
	fd3.close()

urlListLvl1.sort()
tmpFD4 = 1
print "LVL 2"
fd4 = open ("/tmp/lvl3-list.url", "w")
for url in urlListLvl1:
	flag = 0
	menu = ""
	getUrl(url, "/tmp/lvl2-"+str(tmpFD4))
	for line in open("/tmp/lvl2-"+str(tmpFD4), "r"):
		if "search-single-navigator" in line:
			flag = 1
		if flag == 1 and ("<h3 class=" in line):
			menu = line.split("\"")[1]
		if flag == 1 and "<ul class=\""+menu.lower()+"\">" in line.lower():
			flag = 2
		if flag == 2 and "<a href" in line:
			fd4.write(line.split("\"")[1])
			print line.split("\"")[1]
		if flag == 2 and "</ul>" in line:
			flag = 1
	tmpFD4 += 1
	break
fd4.close()

print "LVL 3"
tmpFD5 = 1
for line in open("/tmp/lvl3-list.url", "r"):
	if getUrl(line, "/tmp/lvl3-"+str(tmpFD5)+".html"):
		for line in open("/tmp/lvl3-"+str(tmpFD5)+".html", "r"):
			if "<h3><a title=" in line:
				print "/tmp/lvl4-"+str(tmpFD5)+".html", line.split("\"")[3]
				getUrl(line.split("\"")[3], "/tmp/lvl4-"+str(tmpFD5)+".html")
			tmpFD5 += 1
	break

print "LVL 4"
tmpFD6 = 1
for line in open("/tmp/lvl4-"+str(tmpFD6)+".html", "r"):
	if "sku-ean-code" in line:
		print "REF: "+ line.split(">")[1].split("<")[0]
	if "skuBestPrice" in line:
		print "Price: "+line.split(">")[2].split("<")[0]
	tmpFD6 += 1
