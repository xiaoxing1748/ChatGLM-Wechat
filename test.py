from service.config_loader import ConfigLoader
import service.api.qianfan_api as qianfan

if __name__ == "__main__":
    config = ConfigLoader()
    appid = config.get_qianfan_config("appid")
    sdkaccesskey = config.get_qianfan_config("sdkaccesskey")
    sdksecretkey = config.get_qianfan_config("sdksecretkey")
    model = config.get_qianfan_config("model")
    resp = qianfan.qianfan_chat(sdkaccesskey, sdksecretkey, "你好", appid, model)
    print(resp)
