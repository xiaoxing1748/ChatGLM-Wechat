import logging
import datetime
from flask import Flask
from flask import request
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy import parse_message
from wechatpy.replies import create_reply
from wechatpy.replies import TextReply
from wechatpy import WeChatClient
# from transformers import AutoTokenizer, AutoModel
import time
from threading import Thread
# import chatTest
import config_reader
import api.qianfan_api as qianfan


app = Flask(__name__)
app.debug = True
print("启动于:", datetime.datetime.now())
handler = logging.StreamHandler()
app.logger.addHandler(handler)


# 公众号信息
appid, appsecret, token = config_reader.get_wechat_config()
url = config_reader.get_url()
# 公众号客户端配置
client = WeChatClient(appid, appsecret)

# 千帆信息
qianfan_appid, qianfan_apikey, qianfan_secretkey, qianfan_serviceid = config_reader.get_qianfan_config()

# tokenizer = AutoTokenizer.from_pretrained(
#     r"F:\ChatGLM\model", trust_remote_code=True)
# model = AutoModel.from_pretrained(
#     r"F:\ChatGLM\model", trust_remote_code=True).cuda()


def asyncTask(source, content):
    print("提问:source:{}, content:{}".format(source, content))
    # response, history = model.chat(tokenizer, content, history=[])
    # response = chatTest.chat(content)
    response = qianfan.chat(qianfan_apikey, qianfan_secretkey, content)
    print("回答:reply:{}".format(response))
    # time.sleep(10)
    client.message.send_text(source, response)


# 简易的回复测试
def reply_msg(msg):
    print("提问:source:{}, content:{}".format(
        msg.source, msg.content))
    response = "已收到信息"
    print("回答:reply:{}".format(response))
    # reply=create_reply(response, msg)
    reply = TextReply(content=response, message=msg)
    return reply.render()


@app.route(url, methods=['GET', 'POST'])
def wechat():
    # 服务器配置验证
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    if request.method == 'GET':
        # 接收参数 token, signature, timestamp, nonce
        echostr = request.args.get("echostr")
        signature = request.args.get("signature")
        if echostr:
            print("request timestamp:{},nonce:{}, echostr:{}, signature:{}".format(timestamp,
                                                                                   nonce, echostr, signature))
            try:
                check_signature(token, signature, timestamp, nonce)
                return echostr
            except InvalidSignatureException:
                print("invalid message from request")
    # 回复功能
    else:
        xml = request.data
        if xml:
            try:
                msg = parse_message(xml)
                # print("message from wechat msg:{}".format(msg))

                t1 = Thread(target=asyncTask, args=(msg.source, msg.content))
                t1.start()
                return "success"

                # 简易的回复测试
                # response = reply_msg(msg)
                # return response

            except (InvalidAppIdException, InvalidSignatureException):
                print("cannot decrypt message!")
        else:
            print("no xml body, invalid request!")
    return ""


if __name__ == '__main__':
    print('starting wechat of chatGLM')
    app.run(host='127.0.0.1', port=9000, debug=True)
