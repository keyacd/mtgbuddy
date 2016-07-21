import logging
import urllib2
import urllib2
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------
def returnmtginfo(cardname):
        final_query = ""
        cardname = cardname.replace(' ','+')
        try:
                url = "http://magiccards.info/query?q=" + cardname + "&v=card&s=cname"
                sock = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
                cardname.replace('+',' ')
                final_query = "Error: '" + cardname + "' could not be found."
                return final_query
        else:
                soup = BeautifulSoup(sock.read(), 'html.parser')
                table = soup.find('table',attrs={'class':None,'border':'0','cellpadding':'0','cellspacing':'0','width':'100%','align':'center','style':'margin: 0 0 0.5em 0;'})
                img_table = str(table).split('\n')
                
                if len(img_table) >= 3:
                        img1 = img_table[3]
                        img2 = img_table[4]
                else:
                        cardname = cardname.replace('+',' ')
                        if debug:
                                print url
                        final_query = "Error: '" + cardname + "' could not be found."
                        return final_query
                table = table.get_text().split('\n')
                table2 = []
                for i in range(0,len(table)):
                        line = table[i].encode('utf-8').strip()
                        if line != "":
                                table2.append(line)
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
                
                final_query = imglink[5:-1]
                final_query += "\n" + table2[0] + "\n" + table2[1] + "\n" + table2[3] + "\n--------------------------------------"
                return final_query

# -------------------------------------------------------------------------------------------------------
class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id,msg):
        txt = "Hi, I'm MTG Buddy! I can fetch Magic: the Gathering cards for you using magiccards.info!\n"
        txt = txt + "Just type my name and then a card name (and/or any of the syntax listed at magiccards.info/syntax.html), and I'll find the closest match!\n"
        txt = txt + "If you ever want to see this message again, type my name and then help?"
        txt += " You typed in: " + msg
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id, msg):
        #msg is the card name at the moment
        txt = returnmtginfo(msg)
        self.send_message(channel_id, txt)
        '''
        # Sorry Darien, imma comment out this current code for now
        card_name = msg.replace("d", "")
        if card_name == "" or card_name == " ":
            txt = card_name+"? I don't understand!\n"
            txt = txt + "I can't find a card if you don't give me a name!\n"
            txt = txt + "If you're confused, just type my name and then help?"
            self.send_message(channel_id, txt)
        else:
            search_name = card_name.replace(" ", "+")
            txt = "Searching for "+card_name+"..."
            card_url = "http://www.magiccards.info/query?q="+search_name+"&v=card&s=cname"
            response = urllib2.urlopen(card_url)
            html = response.read()
            html = html.decode('utf-8')
            html = html.split('<td width=\"312\" valign=\"top\">')
            #html = html[1]
            #html = html.split('alt=')
            #img_url = "http://magiccards.info/scans/en/c13/198.jpg" #temp
            #get_name = html
            get_name = "bluh"
            #img_url = html[0]
            #img_url = img_url.split('src=')
            #img_url = img_url[1]
            #img_url = img_url.replace('\"', "")
            #get_name = html[1]
            #get_name = get_name.split(" width")
            #get_name = get_name[0]
            #get_name = get_name.replace('\"', "")
            attachment = {
                "pretext": "Found "+get_name+"!",
                "title": "View "+get_name+" on magiccards.info",
                "title_link": card_url,
                "text": get_name
                #"fallback": card_name,
                #"image_url": img_url,
                #"color": "#7CD197",
            }
            self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
        '''

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)
