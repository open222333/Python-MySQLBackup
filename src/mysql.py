from . import HOST, PORT, USERNAME, PASSWORD, DATABASE, LOG_LEVEL
from .logger import Log
import subprocess
import pymysql
import os

logger = Log()
logger.set_level(LOG_LEVEL)
logger.set_file_handler()
logger.set_msg_handler()

# 儲存匯出檔案的目錄路徑
output_dir = 'output/directory'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def get_all_tables():
    """取得資料庫中的所有資料表名稱
    """
    # 建立資料庫連線
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    logger.info(f'取得{DATABASE}內所有資料表')
    # 建立資料庫遊標
    cursor = conn.cursor()
    # 取得資料庫中的所有資料表名稱
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    # 關閉資料庫連線
    cursor.close()
    conn.close()
    return tables


def mysqldump_table(table: str):
    """匯出資料表

    Args:
        table (str): 資料表名稱
    """
    # 使用pymysql匯出
    # command = f"SELECT * INTO OUTFILE '{output_dir}/{table}.csv' FIELDS TERMINATED BY ',' FROM {table}"
    # cursor.execute(command)

    # 使用mysqldump匯出
    command = f'mysqldump -h {HOST}:{PORT} -u{USERNAME} -p{PASSWORD} {DATABASE} {table} > {output_dir}/{table}.sql'
    logger.info(f'匯出資料表{table} 指令:\n{command}')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # 獲取執行結果
    if result.stdout:
        logger.info(f'匯出資料表 執行結果:\n{result.returncode} - {result.stdout}')
    if result.stderr:
        logger.error(f'匯出資料表 執行結果:\n{result.returncode} - {result.stderr}')
