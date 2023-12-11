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
from threading import Thread
import service.config_reader.config_reader as config_reader
import service.api.qianfan_api as qianfan
import service.api.chatglm_api as chatglm


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


# 已认证公众号的异步回复
def asyncTask(source, content):
    print("提问:source:{}, content:{}".format(source, content))
    response = "已收到信息"

    # 调用本地LangChain
    # response = chatTest.chat(content)

    # 调用千帆ChatGLM
    # response = qianfan.chat(qianfan_apikey, qianfan_secretkey, content)

    # 调用千帆知识库
    # response = qianfan.chat_with_knowledge_base(
    # qianfan_apikey, qianfan_secretkey, qianfan_serviceid, content)

    # 调用本地ChatGLM
    # response = chatglm.chat(content)['response']

    print("回答:reply:{}".format(response))
    client.message.send_text(source, response)


last_responses = {}


# 未认证公众号的同步回复，响应限时5秒
def reply_msg(msg):
    global last_responses  # 引用全局变量

    print("提问:source:{}, content:{}".format(
        msg.source, msg.content))

    # 如果传入的消息是 "/获取回答"，且来源在字典中存在时，返回对应来源的最后 response 信息
    if msg.content == "/获取回答" and msg.source in last_responses:
        response = last_responses[msg.source]
    else:

        response = "已收到信息"

        # 调用本地LangChain
        # response = chatTest.chat(content)

        # 调用千帆ChatGLM
        # response = qianfan.chat(qianfan_apikey, qianfan_secretkey, content)

        # 调用千帆知识库
        # response = qianfan.chat_with_knowledge_base(
        # qianfan_apikey, qianfan_secretkey, qianfan_serviceid, content)

        # 调用本地ChatGLM
        # response = chatglm.chat(content)['response']

        last_responses[msg.source] = response  # 存储最后接收到的 response 信息

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

                # 异步回复
                t1 = Thread(target=asyncTask, args=(msg.source, msg.content))
                t1.start()
                return "success"

                # 同步回复
                # response = reply_msg(msg)
                # return response

            except (InvalidAppIdException, InvalidSignatureException):
                print("cannot decrypt message!")
        else:
            print("no xml body, invalid request!")
    return ""


if __name__ == '__main__':
    print('正在启动公众号后台')
    app.run(host='127.0.0.1', port=9000, debug=True)
