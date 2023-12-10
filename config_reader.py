import yaml


# 读取配置文件
def read_config(file_path="config.yaml"):
    """
    return config_data\n
    """
    try:
        with open(file_path, "r") as file:
            config_data = yaml.safe_load(file)
        return config_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return None


config_data = read_config()


# 获取wechat_config
def get_wechat_config(config_key=None):
    """
    return appid, appsecret, token\n
    获取微信公众号的配置\n
    """
    wechat_config = config_data.get("wechat_config", {})
    appid = wechat_config.get("appid", "")
    appsecret = wechat_config.get("appsecret", "")
    token = wechat_config.get("token", "")
    if config_key is not None:
        # 如果指定了config_key，只返回对应的值
        return wechat_config.get(config_key, "")
    else:
        return appid, appsecret, token


# 获取qianfan_config
def get_qianfan_config(config_key=None):
    """
    return appid, apikey, secretkey, serviceid\n
    获取千帆应用配置\n
    """
    qianfan_config = config_data.get("qianfan_config", {})
    appid = qianfan_config.get("appid", "")
    apikey = qianfan_config.get("apikey", "")
    secretkey = qianfan_config.get("secretkey", "")
    serviceid = qianfan_config.get("serviceid", "")
    if config_key is not None:
        # 如果指定了config_key，只返回对应的值
        return qianfan_config.get(config_key, "")
    else:
        return appid, apikey, secretkey, serviceid


# 获取url
def get_url():
    """
    return url\n
    获取url\n
    """
    url = config_data.get("url", "")
    return url
