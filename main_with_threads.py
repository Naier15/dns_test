import csv
from conn import Conn
from clock import Clock
from config import branches, cities, products, sales
import threading as th
from typing import Callable
import pandas as pd
import queries as query


locker = th.Lock()

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


def to_db(command: str, get_data: Callable) -> None:
    name = th.current_thread().name
    while True:
        try:
            with locker:
                data = get_data()

                if data == ():
                    print(f'[THREAD DONE] {data}')
                    break

                # print(f'Thread {name} working {data}') # to debug
                Conn.execute_many_args(command, data)

        except Exception as e:
            print(f'[THREAD ERROR] Thread {name} is broken', e)


def csv_to_db(db_path: str, command: str, num_processes: int = 5, batch_size: int = 1000000) -> None:  
    threads = []

    csv_file = open(db_path, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    get_data = batch(reader, batch_size)
    
    for _ in range(num_processes):
        thread = th.Thread(target=to_db, args=(command, get_data), daemon=False)
        threads.append(thread)

    [t.start() for t in threads]
    print('Started')

    [t.join() for t in threads]
    print('Well done!')

    csv_file.close()
    

def main() -> None:
    clock = Clock()
    # Conn.instanciate() # Uncommit if there isn't database with tables
    Conn.connect()

    # Uploaing csv tables to database
    # csv_to_db(cities, query.insert_cities_command)
    # csv_to_db(products, query.insert_products_command)
    # csv_to_db(branches, query.insert_branches_command)
    # csv_to_db(sales, query.insert_sales_command)

    # Conn.execute_many_commands(query.set_indexes)

    Conn.disconnect()
    clock.stop()


if __name__ == '__main__':
    main()