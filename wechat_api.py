import logging
import datetime
from flask import Flask
from flask import request
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy import parse_message
# from wechatpy.replies import create_reply
from wechatpy.replies import TextReply
from wechatpy import WeChatClient
from threading import Thread
from config_loader import ConfigLoader as config
import qianfan_api as qianfan
import chatglm_api as chatglm
import faiss_vector_store as faiss_vector_store
import knowledge_chain as knowledge_chain
import embeddings
import json


print("启动于:", datetime.datetime.now())
app = Flask(__name__)
handler = logging.StreamHandler()
app.logger.addHandler(handler)

config = config()
# 公众号信息
wechat_appid = config.get_wechat_config("appid")
wechat_appsecret = config.get_wechat_config("appsecret")
wechat_token = config.get_wechat_config("token")
url = config.get_url_path()
# 公众号客户端配置
client = WeChatClient(wechat_appid, wechat_appsecret)


# 加载embedding
embedding = embeddings.load()
# 向量存储
document_path = "./document/news.txt"
vector_store = ""
vector_store = faiss_vector_store.index(document_path, embedding)


# 回复缓存
response_dict = {}


def save_responses(msg, response, response_dict, max_entries=10):
    # 将新的键值对添加到字典中
    response_dict[msg.source] = response

    # 如果字典中的键值对数量超过了最大限制，删除最早的键值对
    if len(response_dict) > max_entries:
        # 获取字典的所有键并按照插入顺序排序
        sorted_keys = list(response_dict.keys())

        # 删除最早的键值对
        del response_dict[sorted_keys[0]]


# 生成回答
def getresponse(msg):
    docs = faiss_vector_store.search(msg.content, document_path, vector_store)
    # 本地ChatGLM
    if msg.content.startswith("/a "):
        question = msg.content.split("/a ")[1]
        response = chatglm.chat(question)['response']
        save_responses(msg, response, response_dict)
        print(response_dict)
        return response
    # 本地QAChain
    if msg.content.startswith("/b "):
        question = msg.content.split("/b ")[1]
        response = knowledge_chain.qa_chain_legacy(question, vector_store)
        save_responses(msg, response, response_dict)
        print(response_dict)
        return response
    # 千帆ChatGLM
    if msg.content.startswith("/c "):
        question = msg.content.split("/c ")[1]
        response = qianfan.chat(question).text
        response = json.loads(response)["result"]
        save_responses(msg, response, response_dict)
        print(response_dict)
        return response
    # 千帆QAChain
    if msg.content.startswith("/d "):
        question = msg.content.split("/d ")[1]
        response = knowledge_chain.qianfan_chain(question, docs).text
        response = json.loads(response)["result"]
        save_responses(msg, response, response_dict)
        print(response_dict)
        return response
    # 千帆知识库
    if msg.content.startswith("/e "):
        question = msg.content.split("/e ")[1]
        response = qianfan.chat_with_knowledge_base(question).text
        response = json.loads(response)["result"]
        save_responses(msg, response, response_dict)
        print(response_dict)
        return response
    else:
        response = "已收到信息"
        save_responses(msg, response, response_dict)
        print(response_dict)
        return response


# 已认证公众号的异步回复
def async_reply_msg(msg):
    print("source:{}\ncontent:{}".format(msg.source, msg.content))
    response = getresponse(msg)
    print("response:{}\n".format(response))
    client.message.send_text(msg.source, response)


# 未认证公众号的响应回复，响应限时5秒
def reply_msg(msg):
    # response = getresponse(msg)
    # 备注：响应回答超时会重试三次，因此响应回答只能用来做获取回答功能，不能用来做聊天功能
    if msg.content == "/获取回答" and msg.source in response_dict:
        response = f"您最近一次提问的回答是：{response_dict[msg.source]}"
        print("回答:reply:{}".format(response))
        reply = TextReply(content=response, message=msg)
        return reply.render()
    else:
        return None


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
                check_signature(wechat_token, signature, timestamp, nonce)
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
                t1 = Thread(target=async_reply_msg, args=(msg,))
                t1.start()

                # 同步回复
                response = reply_msg(msg)
                if response is not None:
                    return response
                return "success"

            except (InvalidAppIdException, InvalidSignatureException):
                print("cannot decrypt message!")
        else:
            print("no xml body, invalid request!")
    return ""


if __name__ == '__main__':
    print('正在启动公众号后台')
    app.run(host='127.0.0.1', port=9000, debug=False)
    # docs = faiss_vector_store.search("question", "./document/news.txt")
    # print(knowledge_chain.qianfan_chain("什么啤酒好喝？", docs))
    # print(qianfan.chat_with_knowledge_base("你好"))
    # print(qianfan.chat("你好"))
    # print(qianfan.get_access_token())
