#!/usr/bin/python

import urllib2
import re  # this actually stands for regular expression
from bs4 import BeautifulSoup

# -----------------------------------------------------------
def returnmtginfo(cardname, debug):
        cardname = cardname.replace(' ','+')
        try:
                url = "http://magiccards.info/query?q=" + cardname + "&v=card&s=cname"
                sock = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
                cardname.replace('+',' ')
                print url
                print "Error: '" + cardname + "' could not be found."
                return ""
        else:
                soup = BeautifulSoup(sock.read(), 'html.parser')
                # returns an array of three strings, i.e.:
                #['21  Members', '21  Watchers', '66  Pageviews']
                #stats = filter(None,str((soup.find("div", {"id": "super-secret-stats"})).get_text()).split("\n"))
                #icon_url = soup.find("meta",{"property":"og:image"})['content']
                #if icon_url == 'http://a.deviantart.net/avatars/default.gif':
                #        return 'http://a.deviantart.net/avatars/default_group.gif'
                #else:
                #        return icon_url
                table = soup.find('table',attrs={'class':None,'border':'0','cellpadding':'0','cellspacing':'0','width':'100%','align':'center','style':'margin: 0 0 0.5em 0;'})
                img_table = str(table).split('\n')
                
                if len(img_table) >= 3:
                        img1 = img_table[3]
                        img2 = img_table[4]
                else:
                        cardname = cardname.replace('+',' ')
                        if debug:
                                print url
                        print "Error: '" + cardname + "' could not be found."
                        return
                
                table = table.get_text().split('\n')
                table2 = []
                for i in range(0,len(table)):
                        line = table[i].encode('utf-8').strip()
                        if line != "":
                                table2.append(line)

                #returnimgurl
                if img2.startswith('<img alt='):
                        img2 = img2.split(' ')
                        imglink = ""
                        for i in range(0,len(img2)):
                                if img2[i].startswith('src="'):
                                        imglink = img2[i]
                                        break
                else:
                        img1 = img1.split(' ')
                        imglink = ""
                        for i in range(0,len(img1)):
                                if img1[i].startswith('src="'):
                                        imglink = img1[i]
                                        break
                
                print imglink[5:-1]
                print table2[0]
                print table2[1]
                print table2[3]
                print "--------------------------------------"
                return

debug = True
cflag = "0"
while cflag != "1":
        cflag = raw_input("\nEnter card query or 1 to exit: ",)
        if cflag != "1":
                returnmtginfo(cflag,debug)




