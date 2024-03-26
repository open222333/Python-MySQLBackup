from src import LOG_LEVEL
from src.logger import Log
from pprint import pformat
from pymysql.cursors import DictCursor
from pymysql import Connection
import subprocess
import pymysql.cursors
import os


class MySQLConnect:

	def __init__(self, **kwargs) -> None:
		self.logger = Log('MySQLConnect')
		self.log_level = str(kwargs.get('log_level', LOG_LEVEL)).upper()
		self.logger.set_level(self.log_level)
		self.logger.set_msg_handler()

		# mysql 連線設定
		self.mysql_host = kwargs.get('mysql_host', '127.0.0.1')
		self.mysql_port = int(kwargs.get('mysql_port', 3306))
		self.mysql_database = kwargs.get('mysql_database')
		self.mysql_username = kwargs.get('mysql_username')
		self.mysql_password = kwargs.get('mysql_password')
		self.charset = kwargs.get('charset', 'utf8mb4')
		self.autocommit = bool(kwargs.get('autocommit', True))
		self.test = False
		self.err_logger = Log('MySQLConnect Error')

	def enable_err_logfile(self):
		"""啟用 錯誤 log 檔案紀錄
		"""
		self.err_logger.set_file_handler()


	def get_mysql_connect(self, **kwargs):
		"""取得 mysql 連線

		Returns:
		    _type_: _description_
		"""
		try:
			host = kwargs.get('host', self.mysql_host)
			port = int(kwargs.get('port', self.mysql_port))
			database = kwargs.get('database', self.mysql_database)
			username = kwargs.get('username', self.mysql_username)
			password = kwargs.get('password', self.mysql_password)
			charset = kwargs.get('charset', self.charset)
			autocommit = bool(kwargs.get('autocommit', self.autocommit))
			name = kwargs.get('name')

			mysql_connect = pymysql.connect(
				host=host,
				port=port,
				user=username,
				password=password,
				database=database,
				charset=charset,
				autocommit=autocommit,
				cursorclass=DictCursor
			)

			mysql_setting = {
				'mysql_host': host,
				'mysql_port': port,
				'mysql_database': database,
				'mysql_username': username,
				'mysql_password': password,
				'charset': charset,
				'autocommit': autocommit
			}

			if name:
				mysql_setting['name'] = name

			self.logger.debug(f'mysql_connect 設定:\n{pformat(mysql_setting, sort_dicts=False)}')
			return mysql_connect
		except Exception as err:
			self.logger.error(f'取得 mysql 連線 發生錯誤: {err}\n設定:\n{pformat(mysql_setting, sort_dicts=False)}', exc_info=True)



class MySQLBackup(MySQLConnect):

	def __init__(self, output_dir: str, **kwargs) -> None:
		super().__init__(**kwargs)

		self.logger = Log('MySQLConnect')
		self.log_level = str(kwargs.get('log_level', LOG_LEVEL)).upper()
		self.logger.set_level(self.log_level)
		self.logger.set_msg_handler()
		# 儲存匯出檔案的目錄路徑
		self.output_dir = output_dir
		if not os.path.exists(self.output_dir):
			os.makedirs(self.output_dir)

	def get_all_tables(self):
		"""取得資料庫中的所有資料表名稱
		"""
		# 建立資料庫連線
		conn = pymysql.connect(
			host=self.mysql_host,
			port=self.mysql_port,
			user=self.mysql_username,
			password=self.mysql_username,
			database=self.mysql_database
		)
		self.logger.info(f'取得{self.mysql_database}內所有資料表')
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
		command = f'mysqldump -h {self.mysql_host}:{self.mysql_port} -u{self.mysql_username} -p{self.mysql_password} {self.mysql_database} {table} > {self.output_dir}/{table}.sql'
		self.logger.info(f'匯出資料表{table} 指令:\n{command}')
		result = subprocess.run(command, shell=True, capture_output=True, text=True)
		# 獲取執行結果
		if result.stdout:
			self.logger.info(f'匯出資料表 執行結果:\n{result.returncode} - {result.stdout}')
		if result.stderr:
			self.logger.error(f'匯出資料表 執行結果:\n{result.returncode} - {result.stderr}')

	def mysqldump_all_tables(self):
		"""匯出 指定資料庫 所有資料表
		"""
		tables = self.get_all_tables()
		total_num = len(tables)
		for index in range(total_num):
			print(f'{index + 1}/{total_num}')
			self.mysqldump_table(tables[index][0])
