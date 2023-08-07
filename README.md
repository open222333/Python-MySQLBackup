# Python-MySQL_Backup

# 用法

## main-backup.py

```ini
[SETTING]
; 設定主機資訊json檔路徑 預設值 conf/host.json
; HOST_JSON_PATH=

; 設定輸出路徑 預設值 output/
; OUTPUT_PATH=
```

```json
[
  {
    "execute": false, // 是否執行
    "host": "", // 主機名稱 或 ip
    "port": null, // 端口 預設3306
    "username": "", // mysql用戶
    "password": "", // mysql密碼
    "databases": [ // 資料庫
      "database1",
      "database2"
    ],
    "tables": [ // 資料表
      "table1",
      "tables2"
    ],
    "note": "" // 備註用
  },
  {
    "execute": false,
    "host": "",
    "port": null,
    "username": "",
    "password": "",
    "databases": [
      "database2"
    ],
    "tables": [
      "table1",
      "tables2"
    ],
    "note": ""
  }
]
```

```bash
usage: main-backup.py [-h] [-o OUTPUT] [-a]

備份mysql資料表

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        輸出資料夾
  -a, --all             匯出所有資料表
```