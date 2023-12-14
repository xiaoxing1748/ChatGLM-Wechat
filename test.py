from service.config_loader import ConfigLoader

config = ConfigLoader()
url = config.get_url_path()
print(url)
