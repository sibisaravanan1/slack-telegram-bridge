from slackeventsapi import SlackEventAdapter
import slack_sdk
from slack_sdk.errors import SlackApiError
import telebot
import os
from asyncio import events
from distutils.log import debug
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask
import requests

app = Flask(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SLACK_SIGNING_SECRET=os.environ['SLACK_SIGNING_SECRET']
SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN']
SLACK_EVENT_REQUEST_URL=os.environ['SLACK_EVENT_REQUEST_URL']
TELEGRAM_BOT_TOKEN=os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_BOT_CHAT_ID=os.environ['TELEGRAM_BOT_CHAT_ID']
TELEGRAM_BRIDGE_GROUP_ID=os.environ['TELEGRAM_BRIDGE_GROUP_ID']

slack_event_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET,SLACK_EVENT_REQUEST_URL,app)
SLclient = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)
BOT_ID = SLclient.api_call('auth.test')['user_id']
 
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + TELEGRAM_BRIDGE_GROUP_ID + '&parse_mode=Markdown&text=' + text
    response = requests.get(send_text)

if __name__  == "__main__":
    app.run(debug=True)
