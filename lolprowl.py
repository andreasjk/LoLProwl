# -*- coding: utf-8 -*-

import prowlpy
import httplib2
import json
import sys

class LoLProwl(object):
    """ League of Legends server status Prowler """

    def __init__(self, cron):
        # Settings
        self.apikey = "xxxxxxxxxxxxxxxxxxx"
        self.lolurl = "http://beta.leagueoflegends.com/launcher/content.php"
        self.statusfile = ".lolprowl.tmp"
        self.prowl_priority = 0
        
        # Create the prowl object
        self.prowl = prowlpy.Prowl(self.apikey)

        # Create the http object
        h = httplib2.Http()

        resp,content = h.request(self.lolurl, "GET")
        
        # Make sure we got a proper response
        if resp['status'] != '200':
            raise Exception("Get status Failed: %s" % resp)
        
        #clean up content
        content = content.replace("refreshContent(", "")
        content = content.replace(");", "")
        content = content.replace('\n', "")
        
        data = json.loads(content)
        # print json.dumps(data , sort_keys=True, indent=4)

        # 0 = offline, 1 = online, 2 = busy
        status = data["serverStatus"]

        lastStatus = self.lastStatus()

        if(status != lastStatus):
            if(status == 0):
                # print "Server is now OFFLINE!"
                self.sendStatus("OFFLINE")
            elif(status == 1):
                # print "Server is now ONLINE!"
                self.sendStatus("ONLINE")
            elif(status == 2):
                # print "Server is now BUSY!"
                self.sendStatus("BUSY")
            else:
                # print "Server is now UNKNOWN!"
                self.sendStatus("UNKNOWN")
        
        self.writeStatus(status)
        
    def sendStatus(self, msg):
        try:
            self.prowl.add('League of Legends','Server status', msg, self.prowl_priority)
        except Exception, e:
            print e
    
    def lastStatus(self):
        try:
            f = open(self.statusfile, 'rb')
            s = f.read()
            f.close()
            return int(s)
        except:
            return 0
    
    def writeStatus(self, status):
        f = open(self.statusfile, 'wb')
        f.write(str(status))
        f.close()

if __name__ == '__main__':
    # Run once (cron) or continue in loop
    if len(sys.argv) == 2 and sys.argv[1] == 'cron':
        cron = True
    else:
        cron = False

    try:
        LoLProwl(cron)
    except Exception, e:
        print e
    except KeyboardInterrupt:
        print 'Exiting..'
