import logging
import datetime
from flask import Flask
from flask import request
import sys
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy import parse_message
from wechatpy.replies import create_reply
from wechatpy.replies import TextReply
from wechatpy import WeChatClient
# from transformers import AutoTokenizer, AutoModel
from threading import Thread
import time

app = Flask(__name__)
app.debug = True

# 公众号信息
client = WeChatClient('公众号appid', '公众号secret')
wechatToken = "xiaoxingchat"


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'POST':
        xml = request.data
        if xml:
            try:
                msg = parse_message(xml)
                if msg.type == 'text':
                    print("当前时间:", datetime.datetime.now())
                    print("提问:userId:{}, content:{}".format(
                        msg.source, msg.content))
                    response = "已收到信息"
                    print("当前时间:", datetime.datetime.now())
                    print("回答:chat-GLM replay:{}".format(response))
                    # 等待5秒执行，但响应式只有五秒等待时间
                    # time.sleep(5)
                    # 下面两条都可用
                    # reply=create_reply(response, msg)
                    reply = TextReply(content=response, message=msg)
                    return reply.render()
            except InvalidSignatureException:
                print("invalid message from request")


if __name__ == '__main__':
    print('starting wechat of chatGLM')
    app.run(host='127.0.0.1', port=9000, debug=True)
