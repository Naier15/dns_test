import os


user = 'postgres'
database = 'postgres'
password = os.environ['psql_passwd']
host = '127.0.0.1'
port = '5432'

__path_to_tables = './test_data/'
__ext_tables = '.csv'


# Path to csv tables
branches = f'{__path_to_tables}t_branches{__ext_tables}'
cities = f'{__path_to_tables}t_cities{__ext_tables}'
products = f'{__path_to_tables}t_products{__ext_tables}'
sales = f'{__path_to_tables}t_sales{__ext_tables}'