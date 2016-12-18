#!/usr/bin/env python

import yaml

def loadConfig():
    with open('config/master_config.yaml', 'r') as config_load:
        try:
            loaded_config = yaml.load(config_load)
            return loaded_config
        except yaml.YAMLError as exc:
            print exc