import os
import requests
from flask import Flask, request
import logging

from response_message import GenerateResponseMessage

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v3.1/me/messages'
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN_FACEBOOK')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN_FACEBOOK')


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    response = GenerateResponseMessage(message)
    response_message = response.generate_response()
    send_message(sender, response_message)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

def send_message(recipient_id, text):
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
        events = payload['entry'][0]['messaging']
        for event in events:
            if is_user_message(event):
                text = event['message']['text']
                sender_id = event['sender']['id']
                respond(sender_id, text)

        return True
