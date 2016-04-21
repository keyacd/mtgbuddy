import logging
import urllib2

logger = logging.getLogger(__name__)


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

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "Hi, I'm MTG Buddy! I can fetch Magic: the Gathering cards for you!\n"
        txt = txt + "Just type my name and then a card name, and I'll use Gatherer to find the closest match!\n"
        txt = txt + "If you ever want to see this message again, type my name and then help?"
        self.send_message(channel_id, txt)
    
    def get_card_name(self, bot_name, msg):
        bot_name = "@"+bot_name
        card_name = msg.replace(bot_name+": ", "")
        card_name = msg.replace(bot_name+":", "")
        card_name = card_name.replace(bot_name+" ", "")
        card_name = card_name.replace(bot_name, "")
        card_name = card_name.replace("<>", "")
        return card_name
    
    def get_title(self, html):
        get_name = html.split("</title>")
        get_name = get_name[0]
        get_name = get_name.split("<title>")
        get_name = get_name[1]
        if "(" in get_name:
            get_name.split("(")
            get_name = get_name[0]
        return get_name

    def get_image_url(self, html):
        img_url = html.split("<td width="312" valign="top">")
        img_url = img_url[1]
        img_url = img_url.splig("<img src=")
        img_url = img_url[1]
        img_url = img_url.split("alt")
        img_url = img_url[0]
        img_url = img_url.replace(' " ', "")
        return img_url

    def write_prompt(self, channel_id, msg):
        bot_uid = self.clients.bot_user_id()
        card_name = self.get_card_name(bot_uid, msg)
        if card_name == "" or card_name == " ":
            txt = card_name+"? I don't understand!\n"
            txt = txt + "I can't find a card if you don't give me a name!\n"
            txt = txt + "If you're confused, just type my name and then help?"
            self.send_message(channel_id, txt)
        else:
            search_name = card_name.replace(" ","+")
            txt = "Searching for "+card_name+"..."
            card_url = "http://www.magiccards.info/query?q="+search_name+"&v=card&s=cname"
            response = urllib2.urlopen(card_url)
            html = response.read()
            get_name = self.get_title(html)
            if get_name == card_name:
                #this means there's more than one result for that name
            img_url = self.get_image_url(html)
            attachment = {
                "pretext": "Found "+get_name+"!",
                "title": "View "+get_name+" on magiccards.info",
                "title_link": card_url,
                "text": get_name,
                "fallback": card_name,
                "image_url": img_url,
                "color": "#7CD197",
            }
            self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)
