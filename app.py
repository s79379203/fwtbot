# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第四章 選單功能
多樣版組合按鈕CarouselTemplate
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
# import pandas as pd
# df = pd.read_csv("c:\\users\\elvis\\Desktop\\PyCode\\mails.csv")
# js = df.to_json(orient = 'records',  force_ascii=False)
# data = df.to_string()
# data = 'total input is ' + str(10) +'USD'
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('7BzW5LqyzXzq+Vp9mP3EWjHGTgmto7ogCBc1QftEcMGkwauHpQ5crcBQbER/BbzeLa4BdmIsd4a/jeqEkxU/K4dTSprIDTMzadRo8JOIa+jdoyeWFxpZRlifWR4SsKhEyCx2JLRGdHHTSULjBFPN8gdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('e07acd6e4cf0a0c84272962d4aa9ce0f')
# 主動推播提示資訊: push message
line_bot_api.push_message('U9903430172b3160867439bbc74135845', TextSendMessage(text='歡迎使用FWT小幫手. 請輸入小寫fwt開始!'))

# 監聽所有來自 /callback 的 Post Request
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
# '拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('fwt',message):
        carousel_template  = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/OWciycm.jpg',
                        title='FWT績效',
                        text='接單狀況',
                        actions=[
                            PostbackAction(
                                label='業務接單金額',
                                display_text=data,
                                data='action=接單明細'
                            ),
                            URIAction(
                                label='公司官網',
                                uri='http://www.forward-tech.com.tw/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                        title='FWT績效',
                        text='待開發',
                        actions=[
                            MessageAction(
                                label='未開發',
                                text=data
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='http://www.forward-tech.com.tw/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
                        title='FWT績效',
                        text='待開發2',
                        actions=[
                            MessageAction(
                                label='未開發2',
                                text=data
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='http://www.forward-tech.com.tw/'
                            )
                        ]
                    )
                ]
            )

        # line_bot_api.reply_message(event.reply_token, carousel_template_message)
        template_message = TemplateSendMessage(
        alt_text = 'Carousel alt text', template = carousel_template)

        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式

import sqlite3

import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "CustOrders.db")

try:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall()[2])
    data = '2022年' + '\n'
    totalamt = 0
    avgamt = 0
    for item in cursor.execute("SELECT * FROM OrdersBySales;"):
        data += item[0]+'˙累積接單:'+str(item[1])+'萬'+' 月平均接單:'+str(item[2])+'萬' +'\n'
        print(data)
        totalamt += item[1]
        avgamt += item[2]
    data += '總金額:'+str(totalamt)+'萬 '+'月平均:'+str(round(avgamt,ndigits=1))+'萬 '
    print(data)
    con.close()
except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
