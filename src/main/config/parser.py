import yaml
from loguru import logger

def load_config():
    try:
        config = yaml.full_load(open("src/resource/configs/dev-config.yaml"))
        return config["invalid_reprocess_indexer"]
    except Exception as e:
        logger.error(e)
        raise Exception("Config not found")
