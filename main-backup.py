from src.mysql import MySQLBackup
from src import HOST_INFO, OUTPUT_PATH
from argparse import ArgumentParser

parser = ArgumentParser(description='備份mysql資料表')
parser.add_argument('-o', '--output', type=str, help='輸出資料夾', default=OUTPUT_PATH)
parser.add_argument('-a', '--all', action='store_true', help='匯出所有資料表')
args = parser.parse_args()

if __name__ == "__main__":
    for info in HOST_INFO:
        if info['execute']:
            for database in info['databases']:
                mb = MySQLBackup(
                    host=info['host'],
                    username=info['username'],
                    password=info['password'],
                    database=database,
                    output_dir=args.output
                )

                if info['port']:
                    mb.set_port(int(info['port']))

                if args.all:
                    mb.mysqldump_all_tables()
                else:
                    for table in info['tables']:
                        mb.mysqldump_table(table=table)
