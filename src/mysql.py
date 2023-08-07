from . import LOG_LEVEL
from .logger import Log
import subprocess
import pymysql
import os

logger = Log()
logger.set_level(LOG_LEVEL)
logger.set_file_handler()
logger.set_msg_handler()


class MySQLBackup:

    def __init__(self, host: str, output_dir: str, username: str, password: str, database: str, port: int = 3306) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        # 儲存匯出檔案的目錄路徑
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def set_database(self, database: str):
        """設置 資料庫名稱

        Args:
            database (str): _description_
        """
        self.database = database

    def set_port(self, port: int):
        """設置 端口

        Args:
            port (int): _description_
        """
        self.port = port

    def get_all_tables(self):
        """取得資料庫中的所有資料表名稱
        """
        # 建立資料庫連線
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database
        )
        logger.info(f'取得{self.database}內所有資料表')
        # 建立資料庫遊標
        cursor = conn.cursor()
        # 取得資料庫中的所有資料表名稱
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        # 關閉資料庫連線
        cursor.close()
        conn.close()
        return tables

    def mysqldump_table(self, table: str):
        """匯出資料表

        Args:
            table (str): 資料表名稱
        """
        # 使用pymysql匯出
        # command = f"SELECT * INTO OUTFILE '{output_dir}/{table}.csv' FIELDS TERMINATED BY ',' FROM {table}"
        # cursor.execute(command)

        # 使用mysqldump匯出
        command = f'mysqldump -h {self.host}:{self.port} -u{self.username} -p{self.password} {self.database} {table} > {self.output_dir}/{table}.sql'
        logger.info(f'匯出資料表{table} 指令:\n{command}')
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # 獲取執行結果
        if result.stdout:
            logger.info(f'匯出資料表 執行結果:\n{result.returncode} - {result.stdout}')
        if result.stderr:
            logger.error(f'匯出資料表 執行結果:\n{result.returncode} - {result.stderr}')

    def mysqldump_all_tables(self):
        """匯出 指定資料庫 所有資料表
        """
        tables = self.get_all_tables()
        total_num = len(tables)
        for index in range(total_num):
            print(f'{index + 1}/{total_num}')
            self.mysqldump_table(tables[index][0])
