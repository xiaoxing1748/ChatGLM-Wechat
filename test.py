import config_reader
import api.qianfan_api as qianfan

appid, apikey, secretkey, serviceid = config_reader.get_qianfan_config()
print(appid, apikey, secretkey, serviceid)
# print(apikey, secretkey)

# appid = config_reader.get_wechat_config(["appid"])
# print(appid)


# qianfan.chat(apikey, secretkey, "你好")
# qianfan.chat_with_knowledge_base(
#     apikey, secretkey, serviceid, "今年的招生政策如何？")
