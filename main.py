# coding: utf-8

from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']
DATABASE_URL = os.environ.get('DATABASE_URL')

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route('/')
def hello_world():
    return 'hello world!'


def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def get_response_message(mes_from):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM pokemon_status WHERE name02='{}'".format(mes_from))
            rows = cur.fetchall()
            return rows


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    rows = get_response_message(event.message.text)

    if len(rows)==0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ピカピカー。ピッピカピーピカピカチュウ（このポケモンはガラル地方にはいないよ！）'))
    else:
        r = rows[0]
        reply_message = f'🌟{r[2]}のデータだね🌟\n\n'\
                        f'ガラル図鑑No.{r[0]}\n'\
                        f'タイプ1 {r[10]}\n'\
                        f'タイプ2 {r[11] if r[11] else "なし"}\n'\
                        f'HP {r[3]}\n'\
                        f'こうげき {r[4]}\n'\
                        f'ぼうぎょ {r[5]}\n'\
                        f'とくこう {r[6]}\n'\
                        f'とくぼう {r[7]}\n'\
                        f'すばやさ {r[8]}\n'\
                        f'種族値合計 {r[9]}\n\n'\
                        f'英語名は{r[1]}だよ❗️❗️\n'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message))


if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    app.run(host='0.0.0.0', port=port)