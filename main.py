from src.mysql import get_all_tables, mysqldump_table

tables = get_all_tables()
total_num = len(tables)
for index in range(total_num):
    print(f'{index + 1}/{total_num}')
    mysqldump_table(tables[index][0])
