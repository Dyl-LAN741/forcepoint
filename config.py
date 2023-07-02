# coding: utf-8

# API session configuration
# for read yaml file
import yaml

# path to API key file
PATH = "./config.yml"

file = open(PATH, "r")
config = yaml.load(file)
file.close()

url = config["api_forcepoint"]["url"]
key = config["api_forcepoint"]["key"]
version = config["api_forcepoint"]["version"]
port = config["api_forcepoint"]["port"]

def api_url():
    """Return API url for login session"""
    return url

def api_key():
    """Return API key for login session"""
    return key

def api_version():
    """Return API version for login session"""
    return str(version)

def api_port():
    """Returne API port for login session"""
    return str(port)