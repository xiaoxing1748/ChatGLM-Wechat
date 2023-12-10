import config_reader
import api.qianfan_api as qianfan

appid, apikey, secretkey, serviceid = config_reader.get_qianfan_config()
# print(appid, apikey, secretkey, serviceid)

qianfan.chat(apikey, secretkey, "你好")
