import json


def save_responses(msg, response_dict, max_entries=3):
    # 将新的键值对添加到字典中
    response_dict[msg.source] = msg.content

    # 如果字典中的键值对数量超过了最大限制，删除最早的键值对
    if len(response_dict) > max_entries:
        # 获取字典的所有键并按照插入顺序排序
        sorted_keys = list(response_dict.keys())

        # 删除最早的键值对
        del response_dict[sorted_keys[0]]


class Message:
    def __init__(self, source, content):
        self.source = source
        self.content = content


# 创建一个空的字典来存储响应
response_dict = {}

# 添加一些测试消息
messages = [
    Message("1", "Hello, how are you?"),
    Message("2", "I'm doing well, thanks!"),
    Message("3", "That's great to hear."),
    Message("4", "Hi there!"),
    Message("5", "Hello!"),
    Message("6", "What's up?"),
    Message("7", "Not much, just testing."),
    Message("8", "Seems to be working fine."),
    Message("9", "Good to know!"),
    Message("10", "Thanks!"),
    Message("1", "Hello, how are you?"),
    Message("2", "I'm doing well, thanks!"),
    Message("3", "That's great to hear."),
    Message("4", "Hi there!"),
    Message("5", "Hello!"),
    Message("6", "What's up?"),
    Message("7", "Not much, just testing."),
    Message("8", "Seems to be working fine."),
    Message("9", "Good to know!"),
    Message("10", "Thanks!"),
]

# 逐个添加消息并测试函数
for msg in messages:
    save_responses(msg, response_dict, max_entries=3)
    print("Response Dictionary:")
    for key, value in response_dict.items():
        print(f"{key}: {value}")
    print("--------------------------")

# 打印最终的响应字典
print("Final Response Dictionary:")
for key, value in response_dict.items():
    print(f"{key}: {value}")

    json1 = [{
        "id": "as-bcmt5ct4iy",
        "object": "chat.completion",
        "created": 1702232479,
        "result": "你好！",
        "usage": {
            "prompt_tokens": 2,
            "completion_tokens": 5,
            "total_tokens": 3
        }
    }]
print(json.loads(json1)["result"])
