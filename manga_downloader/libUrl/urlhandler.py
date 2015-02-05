#!/usr/bin/python

import prettyPrint
import urllib2, gzip, time, datetime, httplib, socket, errno
from StringIO import StringIO

logInfo			= prettyPrint.info
logError		= prettyPrint.error

def getUrl (url, fileName):
	file_size = 0
	hr = urllib2.Request(url)
	hr.add_header("User-Agent:", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1")
	hr.add_header("Accept:", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	hr.add_header('Accept-encoding', 'gzip')
	try:
		httpReq = urllib2.urlopen(hr)
	except urllib2.HTTPError:
		logError(url.replace("\n", ""))
		logError("There was an error with HTTP procol. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except urllib2.URLError:
		logError(url.replace("\n", ""))
		logError("There was an error with URL. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except httplib.HTTPException:
		logError(url.replace("\n", ""))
		logError("There was an exception with the HTTP protocol. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except httplib.BadStatusLine:
		logError(url.replace("\n", ""))
		logError("Bad status line. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except socket.timeout:
		logError(url.replace("\n", ""))
		logError("Timeout. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except httplib.IncompleteRead:
		logError(url.replace("\n", ""))
		logError("Stream was incomplete. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except Exception:
		logError(url.replace("\n", ""))
		logError("There was an unknown error. Retryin in 10s...")
		time.sleep(10)
		httpReq = urllib2.urlopen(hr)
		pass
	except SocketError:
		# [Errno 104] Connection reset by peer
		if SocketError.errno == errno.ECONNRESET:
			logError(url.replace("\n", ""))
			logError("There was an unknown error. Retryin in 60s...")
			time.sleep(60)
			httpReq = urllib2.urlopen(hr)
	else:
		file_size = httpReq.headers["Content-Length"]

	if httpReq.info().get('Content-Encoding') == 'gzip':
		try:
			buf = StringIO(httpReq.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		except IOError:
			logError("Cant gunzip the stream")
			return False
	else:
		data = httpReq.read()

	httpReq.close()

	try:
		fd1 = open(fileName, "wb")
		if ("lvl1" in fileName) or ("lvl3" in fileName) or (".jpg" in fileName) or (".png" in fileName) or (".gif" in fileName) or (".jpeg" in fileName):
			fd1.write(data)
		else:
			fd1.write(data.replace("><", ">\n<"))
		fd1.close()
	except:
		logError("Canno't create file "+fileName)
		return False
	else:
		return True, file_size