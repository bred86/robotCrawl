#!/usr/bin/python

import urllib2, gzip, time, datetime
from StringIO import StringIO

def getUrl (url, fileName):
	hr = urllib2.Request(url)
	hr.add_header("User-Agent:", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1")
	hr.add_header("Accept:", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	hr.add_header('Accept-encoding', 'gzip')
	try:
		httpReq = urllib2.urlopen(hr)
	except urllib2.HTTPError:
		print "["+str(datetime.datetime.now())+"][ERROR] "+url
		print "["+str(datetime.datetime.now())+"][ERROR] That was an error with HTTP procol. Retryin in 10s..."
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except urllib2.URLError:
		print "["+str(datetime.datetime.now())+"][ERROR] "+url
		print "["+str(datetime.datetime.now())+"][ERROR] That was an error with URL. Retryin in 10s..."
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except httplib.HTTPException:
		print "["+str(datetime.datetime.now())+"][ERROR] "+url
		print "["+str(datetime.datetime.now())+"][ERROR] That was an exception with the HTTP protocol. Retryin in 10s..."
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except httplib.BadStatusLine:
		print "["+str(datetime.datetime.now())+"][ERROR] "+url
		print "["+str(datetime.datetime.now())+"][ERROR] Bad status line. Retryin in 10s..."
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except socket.timeout:
		print "["+str(datetime.datetime.now())+"][ERROR] "+url
		print "["+str(datetime.datetime.now())+"][ERROR] Timeout. Retryin in 10s..."
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except Exception:
		print "["+str(datetime.datetime.now())+"][ERROR] "+url
		print "["+str(datetime.datetime.now())+"][ERROR] That was an unknown error. Retryin in 10s..."
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass

	if httpReq.info().get('Content-Encoding') == 'gzip':
		try:
			buf = StringIO(httpReq.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		except IOError:
			print "["+str(datetime.datetime.now())+"][ERROR] Cant gunzip the stream"
			return None
	else:
		data = httpReq.read()

	httpReq.close()

	try:
		fd1 = open(fileName, "w")
		if ("lvl1" in fileName) or ("lvl3" in fileName):
			fd1.write(data)
		else:
			fd1.write(data.replace("><", ">\n<"))
		fd1.close()
	except:
		print "["+str(datetime.datetime.now())+"][ERROR]: Canno't create file "+fileName
		return None
	else:
		return True