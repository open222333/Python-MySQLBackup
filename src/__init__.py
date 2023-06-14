from configparser import ConfigParser
import os

config = ConfigParser()
config.read(os.path.join('.config', 'config.ini'))

HOST = config.get('INFO', 'HOST', fallback='127.0.0.1')
PORT = config.getint('INFO', 'PORT', fallback=3306)
USERNAME = config.get('INFO', 'USERNAME', fallback='root')
PASSWORD = config.get('INFO', 'PASSWORD')
DATABASE = config.get('INFO', 'DATABASE')

LOG_PATH = config.get('LOG', 'LOG_PATH', fallback='logs')
LOG_LEVEL = config.get('LOG', 'LOG_LEVEL', fallback='WARNING')

# 建立log資料夾
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
