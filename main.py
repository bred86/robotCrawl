#!/usr/bin/python

import urllib2, gzip, re
from StringIO import StringIO

urlMaster = "http://www.epocacosmeticos.com.br"
urlListLvl1 = []

def getUrl (url, fileName):
	hr = urllib2.Request(url)
	hr.add_header("User-Agent:", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1")
	hr.add_header("Accept:", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	hr.add_header('Accept-encoding', 'gzip')
	httpReq = urllib2.urlopen(hr)
	if httpReq.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(httpReq.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()
	else:
		data = httpReq.read()

	httpReq.close()

	try:
		fd1 = open(fileName, "w")
		if "lvl1" in fileName:
			fd1.write(data)
		else:
			fd1.write(data.replace("><", ">\n<"))
		fd1.close()
	except:
		print "Erro: Canno't create file "+fileName
		return None
	else:
		return True

url = urlMaster + "/marcas"
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
			print line.split("\"")[1]
		if flag == 2 and "</ul>" in line:
			flag = 1
	tmpFD4 += 1