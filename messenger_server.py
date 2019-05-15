import os
from flask import Flask, request
import requests
import logging

from response_message import GenerateResponseMessage

from password import *

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v3.1/me/messages'
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')


def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "オウム返し '{}'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = GenerateResponseMessage(message)
    response_message = response.generate_response()
    send_message(sender, response_message)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

@app.route("/webhook", methods=['GET','POST'])
def listen():
    """webhookイベントのendpointを取得
    """
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"
