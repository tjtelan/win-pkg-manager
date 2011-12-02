#!/usr/bin/env python

########################################################################
# Group: Windows Package Manager A
# Name: Sebastian Imlay
# Group Members: Joshua Stein and Timothy James Telan
# Date: October 15, 2011
# Query database, perform web only given a db object
########################################################################

# re for regex, urllib2 for downloading.
from db_wrapper import *
import re, urllib2, logging

class app:

    # Initialize the application using the database object.
    def __init__(self, appName, dbObject, logFileName):

        #self.logger = logging.getLogger('Application')
        #self.logger.setLevel(logging.DEBUG)

        #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=logFileName, filemode='a')
        self.name = appName
        self.db = dbObject
        self.dlUrl = ''

        #logging.info("Application: Initialized application using database for " + appName + ".")

    # abritrary delete function.
    def __del__(self):
        #logging.info("Application: Done using Application " + self.name + ".")
        pass





    # Queries the database for regex(s) and download site(s) then downloads
    # the webpage and checks the regex against it.
    #
    # Returns Boolean
    def checkUpdates(self):
        #logging.info("Checking for updates for " + self.name + ".")


        validURLQuery, urlList = get_app_urls(self.db, self.name)

        webHtml = ''

        # make sure it's a list.
        if validURLQuery and len(urlList) > 1:

            dlURL = urlList[0]

            f = urllib2.urlopen(str(dlURL))
            webHtml = f.read()
            f.close()

        # Get the url
        validRegxQuery, regexList = get_app_exe_regex(self.db, self.name)
        #self.dl_regex = regexList[0]
        #allReturns = re.findall(self.dl_regex, webHtml, re.IGNORECASE)

        # Pull the version number out of the executable or out of the
        # webpage.

        return False


    # Download the updates - check for updates first.
    # Not complete (obviously)
    def dlUpdates(self):
        print "Application: Updating " + self.name

        validURLQuery, urlList = get_app_urls(self.db, self.name)
        webHtml = ''

        print urlList

        if validURLQuery:

            dlURL = urlList[0]
            #logging.info("Application: Dowloading webpage from: " + dlURL + ".")

            f = urllib2.urlopen(dlURL)
            webHtml = f.read()
            f.close()

        validRegxQuery, regexList = get_app_exe_regex(self.db, self.name)


        allReturns = []
        if validRegxQuery and len(regexList) > 0:
            dl_regex = regexList[0]
            allReturns = re.findall(dl_regex, webHtml, re.IGNORECASE)


        validVersionQuery, versionList = get_app_version(self.db, self.name)

        if(len(allReturns) > 0):

            print("possible executable URL:", allReturns)
            dl_url = allReturns[0]
            dl_url = dl_url.replace('"', '')
            #dl_url = dl_url[6:len(dl_url) - 1]
            print("Dowloading executable from:", dl_url)

            version = ''
            if validVersionQuery:
                version = '.' + versionList[0]

            req = urllib2.urlopen(dl_url)
            output = open(self.name + version + '.exe', 'wb')
            output.write(req.read())
            output.close()



    def getExeURLs(self):
        allReturns = []
        #print 'urllist = ', urlList


        # Get the list of urls from the database.
        validURLQuery, urlList = get_app_urls(self.db, self.name)
        if validURLQuery and urlList != []:
            webHtml = ''

            # assume that the download url is  first in list.
            dlURL = urlList[1]

            print 'Application: Downloading webpage from ' + dlURL

            f = urllib2.urlopen(str(dlURL))
            webHtml = f.read()
            f.close()

            validRegxQuery, regexList = get_app_exe_regex(self.db, self.name)

            #print 'regex list = ', regexList

            if validRegxQuery and len(regexList) > 0:
                for app_regex in regexList:
                    allReturns = allReturns + re.findall(app_regex, webHtml, re.IGNORECASE)

                if allReturns == []:
                    print 'Application: No returns, possibly download url is wrong. Checking other URL.'

                    dlUrl = urlList[0]


                    # Try the other urls.
                    f = urllib2.urlopen(dlURL)
                    webHtml = f.read()
                    f.close()

                    # Apply regex again.
                    for app_regex in regexList:
                        others = re.findall(app_regex, webHtml, re.IGNORECASE)

                    print otherReturns
                    useOthers = raw_input('Use other returns? [y/n]')
                    if useOthers == 'y':
                        allReturns = others


        return allReturns
