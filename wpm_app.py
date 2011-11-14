########################################################################
# Group: Windows Package Manager A
# Name: Sebastian Imlay
# Group Members: Joshua Stein and Timothy James Telan
# Date: October 15, 2011
# Query database, perform web only given a db object
########################################################################

# re for regex, urllib2 for downloading.
import re, urllib2

class app:

    # initialize with name, website, and regex
    def __init__(self, name, downLoadSite, dl_regex):
        # Parameters: Database object
        # log file (in append mode)
    #def __init__(self, downLoadSite, dl_regex):
        self.dlSite = downLoadSite
        self.dl_regex = dl_regex
        self.name = name
        self.dl_url = ''

    def __del__(self):
        pass


    def checkUpdates(self):
        f = urllib2.urlopen(self.dlSite)
        webHtml = f.read()
        allReturns = re.findall(self.dl_regex, webHtml, re.IGNORECASE)

        if(len(allReturns) > 1):
            print "More than one found"
            for i in allReturns:
                print i

            dl_url = allReturns[0][5:]
            # Remove beginning quote
            if dl_url[0] == '"':
                dl_url = dl_url[1:]

            # Remove ending quote
            if dl_url[len(dl_url) - 1] == '"':
                dl_url = dl_url[:len(dl_url) - 1]

            self.dl_url = dl_url

        elif len(allReturns) == 0:
            print "Found none!"
        else:
            dl_url = allReturns[0][5:]
            if dl_url[0] == '"':
                dl_url = dl_url[1:]

            if dl_url[len(dl_url) - 1] == '"':
                dl_url = dl_url[:len(dl_url) - 1]

            print self.name, dl_url
            self.dl_url = dl_url


    # Download the updates
    def dlUpdates(self):

        if self.dl_url == '':
            print 'Dl url is null, scrapping the web page.'
            self.checkUpdates()

        print "Dowloading from:", self.dl_url

        req = urllib2.urlopen(self.dl_url)
        output = open(self.name + '.exe', 'wb')
        output.write(req.read())
        output.close()
