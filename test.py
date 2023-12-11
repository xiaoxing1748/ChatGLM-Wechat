import json
import time
import requests
import service.config_reader.config_reader as config_reader
# import service.api.qianfan_api as qianfan
import service.api.chatglm_api as chatglm

# appid, apikey, secretkey, serviceid = config_reader.get_qianfan_config()
# print(appid, apikey, secretkey, serviceid)
# print(apikey, secretkey)

# appid = config_reader.get_wechat_config(["appid"])
# print(appid)


# qianfan.chat(apikey, secretkey, "你好")
# qianfan.chat_with_knowledge_base(
#     apikey, secretkey, serviceid, "今年的招生政策如何？")

llm_path = config_reader.get_llm_path()
print(chatglm.run_llm(llm_path))
# time.sleep(20)
# url = "http://localhost:8000/"  # 更改为你的API地址
# data = {
#     "prompt": "你好",
#     # 如果需要，你可以在这里添加其他参数，如"history", "max_length", "top_p", "temperature"
# }

# response = requests.post(url, data=json.dumps(data))

# print(response.json())
