from configparser import ConfigParser
import os

config = ConfigParser()
config.read(os.path.join('conf', 'config.ini'))

# logs相關參數
# 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
LOG_DISABLE = config.getboolean('LOG', 'LOG_DISABLE', fallback=False)
# logs路徑 預設 logs
LOG_PATH = config.get('LOG', 'LOG_PATH', fallback='logs')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = config.get('LOG', 'LOG_LEVEL', fallback='WARNING')
# 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 關閉
LOG_FILE_DISABLE = config.getboolean('LOG', 'LOG_FILE_DISABLE', fallback=True)

# 建立log資料夾
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

# 設定主機資訊json檔路徑 預設值 conf/host.json
HOST_JSON_PATH = config.get('SETTING', 'HOST_JSON_PATH', fallback='conf/host.json')
if os.path.exists(HOST_JSON_PATH):
    with open(HOST_JSON_PATH, 'r') as f:
        HOST_INFO = config.loads(f.read())
else:
    HOST_INFO = []

# 設定輸出路徑 預設值 output
OUTPUT_PATH = config.get('SETTING', 'OUTPUT_PATH', fallback='output')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
