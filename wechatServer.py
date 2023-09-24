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
from transformers import AutoTokenizer, AutoModel
from threading import Thread

app = Flask(__name__)
app.debug = True

# 公众号信息
client = WeChatClient('公众号appid', '公众号secret')
wechatToken = "xiaoxingchat"

handler = logging.StreamHandler()
app.logger.addHandler(handler)

# tokenizer = AutoTokenizer.from_pretrained(
#     r"F:\ChatGLM2-6B\model", trust_remote_code=True)
# model = AutoModel.from_pretrained(
#     r"F:\ChatGLM2-6B\model", trust_remote_code=True).cuda()


def asyncTask(userId, content):
    print("当前时间:", datetime.datetime.now())
    print("提问:userId:{}, content:{}".format(userId, content))
    # response, history = model.chat(tokenizer, content, history=[])
    response = "已收到信息"
    print("当前时间:", datetime.datetime.now())
    print("回答:chat-GLM replay:{}".format(response))
    # client.message.send_text(userId, response)
    reply = create_reply(response, content)
    return reply.render()


def reply_msg(msg):
    response = "已收到信息"
    reply = create_reply(response, msg)
    # print("reply:{}".format(reply))
    print(response)
    return reply.render()


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    if request.method == 'GET':
        # token, signature, timestamp, nonce
        echostr = request.args.get("echostr")
        signature = request.args.get("signature")
        if echostr:
            print("request timestamp:{},nonce:{}, echostr:{}, signature:{}".format(timestamp,
                                                                                   nonce, echostr, signature))
            try:
                check_signature(wechatToken, signature, timestamp, nonce)
                return echostr
            except InvalidSignatureException:
                print("invalid message from request")
    else:
        xml = request.data
        if xml:
            try:
                msg = parse_message(xml)
                # print("message from wechat msg:{}".format(msg))

                # t1 = Thread(target=asyncTask, args=(msg.source, msg))
                # t1.start()

                reply_msg(msg)

                # return "success"
            except (InvalidAppIdException, InvalidSignatureException):
                print("cannot decrypt message!")
        else:
            print("no xml body, invalid request!")
    return ""


if __name__ == '__main__':
    print('starting wechat of chatGLM')
    app.run(host='127.0.0.1', port=9000, debug=True)
