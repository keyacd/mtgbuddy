import logging
import random

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

    def write_prompt(self, channel_id, msg):
        bot_uid = self.clients.bot_user_id()
        card_name = msg.replace("@"+bot_uid, "")
        card_name = card_name.replace("<>", "")
        if card_name == "" or card_name == " ":
            txt = "I can't find a card if you don't give me a name!\nIf you're confused, just type my name and then help?"
            self.send_message(channel_id, txt)
        else:
            search = card_name.replace(" ","+")
            txt = "Searching for "+card_name+"..."
            get_name = "UNIMPLEMENTED"
            get_id = "376404"
            attachment = {
                "pretext": "Found "+get_name+"!",
                "title": "Gatherer info for "+get_name+":",
                "title_link": "http://magiccards.info/query?q="+card_name+"&v=card&s=cname",
                "text": card_name,
                "fallback": get_name,
                "image_url": "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid="+get_id+"&type=card",
                "color": "#7CD197",
            }
            self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)
