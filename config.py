import os


user = 'postgres'
database = 'postgres'
password = os.environ['psql_passwd']
host = '127.0.0.1'
port = '5432'


rename_branches = {
    'Unnamed: 0': 'id', 
    'Ссылка': 'ref', 
    'Наименование': 'title',
    'Город': 'ref_city',
    'КраткоеНаименование': 'short_name',
    'Регион': 'region'
}

rename_cities = {
    'Unnamed: 0': 'id', 
    'Ссылка': 'ref', 
    'Наименование': 'title'
}

rename_products = {
    'Unnamed: 0': 'id', 
    'Ссылка': 'ref', 
    'Наименование': 'title'
}

rename_sales = {
    'Unnamed: 0': 'id', 
    'Период': 'datetime', 
    'Филиал': 'ref_branch',
    'Номенклатура': 'ref_product',
    'Количество': 'quantity',
    'Продажа': 'price'
}