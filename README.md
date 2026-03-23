# Python-MySQLBackup

使用 `mysqldump` 備份多台 MySQL 主機的指定資料庫與資料表，輸出 SQL 檔案至本地目錄。

---

## 目錄

- [功能說明](#功能說明)
- [專案結構](#專案結構)
- [執行流程](#執行流程)
- [使用方法](#使用方法)
- [設定檔說明](#設定檔說明)
- [建議注意事項](#建議注意事項)

---

## 功能說明

1. **多主機備份** — 透過 `host.json` 設定多台 MySQL 主機，批次執行備份
2. **指定資料庫與資料表** — 可針對每台主機分別指定要備份的 `databases` 與 `tables`
3. **全資料表備份** — 加上 `-a` 參數可忽略 `tables` 設定，備份整個資料庫的所有資料表
4. **輸出 SQL 檔** — 每個資料表各自輸出一份 `.sql` 備份檔至指定目錄
5. **彈性設定輸出路徑** — 可透過命令列參數或 `config.ini` 自訂輸出目錄

---

## 專案結構

```
Python-MySQLBackup/
├── main-backup.py          # 主程式入口
├── requirements.txt        # 相依套件
├── conf/
│   ├── config.ini.default  # 設定檔範本
│   └── host.json.default   # 主機清單範本
├── src/
│   ├── __init__.py         # 讀取 config.ini 與 host.json
│   └── mysql.py            # MySQLBackup 核心類別（呼叫 mysqldump）
└── output/                 # 預設備份輸出目錄
```

---

## 執行流程

```
執行 main-backup.py
    |
    +--> 解析命令列參數（-o OUTPUT、-a）
    |
    +--> 讀取 conf/config.ini（OUTPUT_PATH、HOST_JSON_PATH）
    |
    +--> 讀取 conf/host.json（主機清單）
    |
    +--> 遍歷主機清單
            |
            +--> execute == false？ --> 跳過
            |
            +--> execute == true
                    |
                    +--> 遍歷 databases
                            |
                            +--> 有 -a 參數？
                            |       |
                            |       +--> 是 --> mysqldump 備份所有資料表
                            |       |
                            |       +--> 否 --> 遍歷 tables，逐一備份
                            |
                            +--> 輸出 .sql 至 output/
```

---

## 使用方法

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

確認系統已安裝 `mysqldump`：

```bash
mysqldump --version
```

### 2. 複製設定檔

```bash
cp conf/config.ini.default conf/config.ini
cp conf/host.json.default conf/host.json
```

### 3. 編輯主機清單

編輯 `conf/host.json`，填入主機資訊並將 `execute` 設為 `true`：

```json
[
  {
    "execute": true,
    "host": "192.168.1.100",
    "port": 3306,
    "username": "backup_user",
    "password": "your_password",
    "databases": ["mydb"],
    "tables": ["users", "orders"],
    "note": "production-db-1"
  }
]
```

### 4. 執行備份

```bash
# 備份 host.json 中指定的資料表
python main-backup.py

# 指定輸出目錄
python main-backup.py -o /backup/mysql/

# 備份所有資料表（忽略 tables 設定）
python main-backup.py -a

# 組合使用
python main-backup.py -a -o /backup/mysql/
```

### 命令列參數說明

```
usage: main-backup.py [-h] [-o OUTPUT] [-a]

備份 MySQL 資料表

options:
  -h, --help            顯示說明並離開
  -o OUTPUT, --output OUTPUT
                        指定輸出資料夾（預設使用 config.ini 中的 OUTPUT_PATH）
  -a, --all             匯出所有資料表（忽略 host.json 中的 tables 設定）
```

---

## 設定檔說明

### conf/config.ini

```ini
[SETTING]
; 主機資訊 JSON 檔路徑，預設 conf/host.json
; HOST_JSON_PATH=

; 備份輸出路徑，預設 output/
; OUTPUT_PATH=
```

### conf/host.json

```json
[
  {
    "execute": false,
    "host": "",
    "port": null,
    "username": "",
    "password": "",
    "databases": ["database1", "database2"],
    "tables": ["table1", "table2"],
    "note": ""
  }
]
```

| 欄位        | 型別    | 說明                                           |
|-----------|---------|------------------------------------------------|
| execute   | boolean | `true` 才會執行備份，`false` 跳過             |
| host      | string  | MySQL 主機位址或 IP                            |
| port      | integer | 連接埠（填 `null` 使用預設 3306）              |
| username  | string  | MySQL 使用者名稱                               |
| password  | string  | MySQL 密碼                                     |
| databases | array   | 要備份的資料庫名稱清單                         |
| tables    | array   | 要備份的資料表名稱清單（使用 `-a` 時忽略）     |
| note      | string  | 備註，僅供辨識用途，不影響執行                 |

---

## 建議注意事項

- **mysqldump 版本** — 請確認本機 `mysqldump` 與目標 MySQL Server 版本相容，版本差異過大可能導致備份失敗
- **帳號權限** — 備份帳號需具備 `SELECT`、`SHOW VIEW`、`LOCK TABLES` 等必要權限，建議建立專屬備份帳號
- **密碼安全** — `host.json` 含有明文密碼，請限制檔案讀取權限（`chmod 600`），切勿提交至版本控制
- **-a 參數** — 使用 `-a` 時會備份整個資料庫，資料量較大時執行時間較長，請注意磁碟空間是否充足
- **輸出檔案命名** — 備份檔案以資料表為單位輸出，建議搭配排程（cron）並在檔名中加入日期，避免覆蓋舊備份
- **網路連線** — 遠端備份時須確保網路連通性及防火牆規則允許 MySQL 連線（預設 3306 port）
