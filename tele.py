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

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SLACK_SIGNING_SECRET=os.environ['SLACK_SIGNING_SECRET']
SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN']
SLACK_EVENT_REQUEST_URL=os.environ['SLACK_EVENT_REQUEST_URL']
SLACK_CHANNEL_ID=os.environ['SLACK_CHANNEL_ID']
TELEGRAM_BOT_TOKEN=os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_BOT_CHAT_ID=os.environ['TELEGRAM_BOT_CHAT_ID']
TELEGRAM_BRIDGE_GROUP_ID=os.environ['TELEGRAM_BRIDGE_GROUP_ID']

SLclient = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)
TGclient = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@TGclient.message_handler(regexp="^[a-zA-Z0-9_]*$")
def handle_text(message):
    content = message.text
    SLclient.chat_postMessage(channel=SLACK_CHANNEL_ID,text=content)
    
TGclient.polling()
