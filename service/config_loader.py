import yaml
import os


class ConfigLoader:
    """配置文件加载器\n
    可指定配置文件路径，否则默认根目录config.yaml\n
    用法：\n
    config_loader = ConfigLoader()\n
    wechat_config = config_loader.get_wechat_config()\n
    或者：\n
    config_loader = ConfigLoader()\n
    wechat_appid = config_loader.get_wechat_config("appid")\n
    """

    def __init__(self, config_file_path=None):
        if config_file_path is None:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            config_file_path = os.path.join(script_dir, "../config.yaml")
        self.config = self.load_config(config_file_path)

    def load_config(self, config_file_path):
        with open(config_file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def get_wechat_config(self, config_key=None):
        if config_key is not None:
            # 如果指定了config_key，只返回对应的值
            return self.config.get('wechat_config').get(config_key)
        else:
            return self.config.get('wechat_config')

    def get_qianfan_config(self, config_key=None):
        if config_key is not None:
            # 如果指定了config_key，只返回对应的值
            return self.config.get('qianfan_config').get(config_key)
        else:
            return self.config.get('qianfan_config')

    def get_llm_path(self):
        return self.config.get('llm_path')

    def get_embedding_path(self):
        return self.config.get('embedding_path')

    def get_url_path(self):
        return self.config.get('url')


if __name__ == '__main__':
    # config_file_path = 'config.yaml'  # 替换为你的config.yaml文件路径
    config_loader = ConfigLoader()

    wechat_config = config_loader.get_wechat_config()
    wechat_config_appid = config_loader.get_wechat_config("appid")

    qianfan_config = config_loader.get_qianfan_config()
    llm_path = config_loader.get_llm_path()
    embedding_path = config_loader.get_embedding_path()
    url = config_loader.get_url_path()

    print("WeChat Config:")
    print(wechat_config)

    print("\nWeChat Config appid:")
    print(wechat_config_appid)

    print("\nQianfan Config:")
    print(qianfan_config)

    print("\nLLM Path:", llm_path)

    print("\nEmbedding Path:", embedding_path)

    print("\nurl Path:", url)
