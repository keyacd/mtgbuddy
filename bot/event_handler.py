import json
import logging
import re

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):
        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        # In reality, mtgbuddy should only be conducting the message event
        
        #if event_type == 'error':
            # error
            #self.msg_writer.write_error(event['channel'], json.dumps(event))
        #elif event_type == 'message':
        if event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        #elif event_type == 'channel_joined':
            # you joined a channel
        #    self.msg_writer.write_help_message(event['channel'])
        #elif event_type == 'group_joined':
            # you joined a private group
        #    self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if not self.clients.is_message_from_me(event['user']):
            msg_txt = event['text']

            if self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@pybot tell me a joke!"
                msg_txt = msg_txt[11:] # takes out the name of the bot
                
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'],msg_txt)
                else if msg_txt.startswith('card'):
                    #msg_txt[5:] only sends over the card name for the search
                    self.msg_writer.write_prompt(event['channel'], msg_txt[5:])
                else:
                    pass
