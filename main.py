import csv
from conn import Conn
from config import branches, cities, products, sales
from typing import Callable
import queries as query


def batch(lst: any, size: int) -> Callable:
    it = iter(lst)
    next(it)
    def wrapper() -> tuple:
        result = []
        nonlocal it
        try:
            [result.append( tuple( next(it)[1:] ) ) for _ in range(size)] #[1:] - deletes first column (id)
            return tuple(result)
        except StopIteration:
            return tuple(result)

    return wrapper


def upload_to_db(command: str, get_data: Callable) -> None:
    print('[INFO] Uploading to db started')
    while True:
        try:
            data = get_data()

            if data == ():
                print(f'[DONE] Uploading is done {data}')
                break

            Conn.execute_many_args(command, data)

        except Exception as e:
            print('[ERROR] Something went wrong while Conn executes many requests', e)


def csv_to_db(db_path: str, command: str, batch_size: int = 1000000) -> None:  
    with open(db_path, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        get_data = batch(reader, batch_size)

        upload_to_db(command, get_data)


def transfer_csv_tables_to_psql() -> None:
    """Uploaing csv tables to database"""

    csv_to_db(cities, query.insert_cities_command)
    csv_to_db(products, query.insert_products_command)
    csv_to_db(branches, query.insert_branches_command)
    csv_to_db(sales, query.insert_sales_command)
    Conn.execute_many_commands(query.set_indexes)


def main() -> None:
    Conn.instanciate() # ! Uncommit if there isn't database
    Conn.connect()
    Conn.execute_many_commands(query.create_tables_commands) #! Uncommit if tables doesnt exist in psql


    transfer_csv_tables_to_psql() # !Uncommit to transfer csv tables to postgresql


    Conn.disconnect()


if __name__ == '__main__':
    main()