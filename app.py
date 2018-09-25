# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import datetime
import random
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn,
    URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
today = datetime.datetime.now().strftime("%m/%d/%Y")
current_time = datetime.datetime.now().strftime("%I:%M %p")



@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if text == 'Today':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            message = 'Hi {username}! Today is {today}. \
                       Do you want to add a record?'.format(
                username=profile.display_name, today=today)
            confirm_template = ConfirmTemplate(text=message, actions=[
                MessageTemplateAction(label='Checkin', text='Checkin'),
                MessageTemplateAction(label='Checkout', text='Checkout'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)

    if text == 'Checkin' or text == 'Checkout':
        htm_password = os.getenv('MYPASSWORD', None)
        sticker_list = ['109', '138', '117', '407', '426']
        line_bot_api.reply_message(
            event.reply_token, [
                StickerSendMessage(
                    package_id="1",
                    sticker_id=random.choice(sticker_list)
                )
            ]
        )
        os.system(
            f"pybot -d report -v USERNAME:CChao -v PASSWORD:{htm_password} \
            -v DATE:{today} -v TIME_NOW:{current_time} \
            -t '{text} Today' case.robot")

    if text == 'PTO':
        htm_password = os.getenv('MYPASSWORD', None)
        sticker_list = ['428', '430', '124', '10', '103']
        line_bot_api.reply_message(
            event.reply_token, [
                StickerSendMessage(
                    package_id="1",
                    sticker_id=random.choice(sticker_list)
                )
            ]
        )
        os.system(
            "pybot -d report -v USERNAME:CChao -v PASSWORD:{htm_password} \
             -v DATE:{today} -t 'Add PTO Today' case.robot".format(
                htm_password=htm_password,
                today=today))

    if text == 'Sick':
        htm_password = os.getenv('MYPASSWORD', None)
        sticker_list = ['120', '416', '424', '403', '422']
        line_bot_api.reply_message(
            event.reply_token, [
                StickerSendMessage(
                    package_id="1",
                    sticker_id=random.choice(sticker_list)
                )
            ]
        )
        os.system(
            "pybot -d report -v USERNAME:CChao -v PASSWORD:{htm_password} \
             -v DATE:{today} -t 'Add Sick Today' case.robot".format(
                htm_password=htm_password,
                today=today))

    if text == 'Settings':
        line_bot_api.reply_message(event.reply_token, TextMessage(
            text="Under Construction! \
            https://www.youtube.com/watch?v=8BIRbNVOuWM \
            &list=PL-UWPlRIl68ot7sj0QmIdD0NWmW6aBZnN"))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
