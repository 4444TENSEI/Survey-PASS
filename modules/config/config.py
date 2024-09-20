import toml


# 读取配置文件
def load_config():
    with open("config.toml", "r", encoding="utf-8") as config_file:
        config = toml.load(config_file)
    return config
