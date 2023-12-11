
import requests
import json


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
