import logging.config
import os
import yaml


class Config:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'log_config.yaml'), 'rt') as log_config:
            logging.config.dictConfig(yaml.safe_load(log_config.read()))
        self.logger = logging.getLogger("EVO")
