
import requests
import json
import os
import qianfan
from config_loader import ConfigLoader as config


# 千帆信息
qianfan_apikey = config.get_qianfan_config("apikey")
qianfan_secretkey = config.get_qianfan_config("secretkey")
qianfan_serviceid = config.get_qianfan_config("serviceid")


# 获取access_token
def get_access_token(apikey, secretkey):
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + \
        apikey+"&client_secret="+secretkey

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


# 聊天功能
def chat(apikey, secretkey, content):
    """
    return response.text\n
    返回示例\n
    {
    "id": "as-bcmt5ct4iy",
    "object": "chat.completion",
    "created": 1702232479,
    "result": "你好！",
    "is_truncated":false,
    "need_clear_history": false,
    "usage": {
        "prompt_tokens": 2,
        "completion_tokens": 5,
        "total_tokens": 3
        }
    }
    """
    print(content)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + \
        get_access_token(apikey, secretkey)

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


# 知识库问答功能
def chat_with_knowledge_base(apikey, secretkey, serviceid, query):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/" + serviceid + "/?access_token=" + get_access_token(apikey, secretkey
                                                                                                                                    )
    # print(url)
    payload = json.dumps({
        "query": query,
        "plugins": ["uuid-zhishiku"],
        "verbose": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


# ChatSDK
def qianfan_chat(accesskey, secretkey, content, appid=None, model=None):
    # 使用安全认证AK/SK鉴权，通过环境变量方式初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
    os.environ["QIANFAN_ACCESS_KEY"] = accesskey
    os.environ["QIANFAN_SECRET_KEY"] = secretkey

    # 通过AppID设置使用的应用，该参数可选；如果不设置该参数，SDK默认使用最新创建的应用AppID；如果设置，使用如下代码，替换示例中参数，应用AppID替换your_AppID
    if appid is not None:
        os.environ["QIANFAN_APPID"] = str(appid)

    chat_comp = qianfan.ChatCompletion()

    # 指定特定模型
    response = chat_comp.do(model="ChatGLM2-6B-32K", messages=[{
        "role": "user",
        "content": content
    }])
    return response
