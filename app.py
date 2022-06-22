# -*- coding: utf-8 -*-
"""
FWT LineBot小幫手
2022.06.21
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
                        thumbnail_image_url='https://i.imgur.com/oINarLO.png',
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
                        thumbnail_image_url='https://i.imgur.com/Lr88MTG.png',
                        title='FWT績效',
                        text='OutPut',
                        actions=[
                            PostbackAction(
                                label='出貨金額',
                                display_text=data2,
                                data='action=出貨金額'
                            ),
                            URIAction(
                                label='公司官網',
                                uri='http://www.forward-tech.com.tw/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/oTj2UaK.png',
                        title='FWT績效',
                        text='Input',
                        actions=[
                            PostbackAction(
                                label='採購金額',
                                display_text=data3,
                                data='action=採購金額'
                            ),
                            URIAction(
                                label='公司官網',
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
    # 查詢order
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall()[2])
    data = '2022年接單' + '\n'
    totalamt = 0
    avgamt = 0
    for item in cursor.execute("SELECT * FROM OrdersBySales;"):
        data += item[0]+'˙累積接單:'+str(item[1])+'萬 \n'+'月平均:'+str(item[2])+'萬 ' +'\n'
        print(data)
        totalamt += item[1]
        avgamt += item[2]
    data += '總金額:'+str(totalamt)+'萬 \n'+'月平均:'+str(round(avgamt,ndigits=1))+'萬 '
    # 查詢output table
    data2 = '2022年1-5月出貨' + '\n'
    totalamt2 = 0
    avgamt2 = 0
    for item in cursor.execute("SELECT * FROM outputbysales"):
        data2 += item[0] + '˙出貨金額:' + str(item[1]) + '萬 \n' + '月平均:' + str(item[2]) + '萬 \n' + '毛利率:'+str(item[5])+'\n'
        print(data2)
        totalamt2 += item[1]
        avgamt2 += item[2]
    data2 += '總金額:' + str(totalamt2) + '萬 \n' + '月平均:' + str(round(avgamt2, ndigits=1)) + '萬 '
    # 查詢input table
    data3 = '2022年input/USD' + '\n'
    totalamt3 = 0
    avgamt3 = 0
    for item in cursor.execute("SELECT * FROM inputbysales"):
        data3 += item[0] + '˙採購金額:' + str(item[1]) + '萬 \n' + '月平均:' + str(item[2]) + '萬 \n'
        print(data3)
        totalamt3 += item[1]
        avgamt3 += item[2]
    data3 += '採購總金額USD:' + str(totalamt3) + '萬 \n' + '月平均USD:' + str(round(avgamt3, ndigits=1)) + '萬 '
    con.close()
except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
