#!/usr/bin/env python
'''
	Author			: Chaitanya Kumar Guduru
	Organization	: Teradata
	Tool			: Version Check Tool
	Module_Name		: Web Parser (using urllib2)
'''

import os
import re
import shutil
import urllib2
from HTMLParser import HTMLParser
from urlparse import urlparse

def downloadFile(url, destDir='.'):
    req = urllib2.Request(url)
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, uname, pswd)

    auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_manager)

    urllib2.install_opener(opener)
    handler = urllib2.urlopen(req)

    if handler.getcode() == 200:
        glog('\nDownloading file ' + url, 3)
        if os.path.basename(urlparse(url).path) == 'release':
            HTMLpage = handler.read()
            return HTMLpage
        else:
            filename = os.path.join(destDir, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as out:
                out.write(handler.read())
    else:
        glog('\nFailed to download ' + url, 2)

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, print it.
                if name == "href":
                    value = value.replace('\n','')
                    path = re.search(r'(.*).(gz|zip|tar|pdf|txt|rpm|exe)$', value, re.I | re.M)
                    if path:
                        download_link = "https://distribution-srvr.asterdata.com" + path.group()
                        downloadFile(download_link, TarFolder)

def parser(releaseNumber, auth, log):
    global TarFolder, uname, pswd, glog

    glog = log
    uname = auth[0]
    pswd = auth[1]
    TarFolder = os.path.join('tempFiles', 'TarFiles_'+releaseNumber)
    URL = "https://distribution-srvr.asterdata.com/release?release=" + releaseNumber
    HTMLpage = downloadFile(URL)

    if os.path.exists(TarFolder):
        shutil.rmtree(TarFolder)
    os.mkdir(TarFolder, 0755)

    log('\nStarting download of ' + releaseNumber + ' into ' + TarFolder, 2)
    parser = MyHTMLParser()
    parser.feed(HTMLpage)
    releaseName = re.search('<title>(.*?)</title>', HTMLpage, re.IGNORECASE | re.DOTALL).group(1)
    log('\nDownload of ' + releaseName + ', successful into ' + TarFolder + '\n')

    return releaseName
