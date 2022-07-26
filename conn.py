from psycopg2 import Error, connect
from config import user, password, host, port, database
from queries import create_tables_commands


class Conn:
    """Class is used for requests to PostgresSQL"""

    __instance = None


    @classmethod
    def instanciate(cls) -> None:
        try:
            cls.connect()
            cls.execute(f"CREATE DATABASE {database};")
            cls.execute(f"ALTER DATABASE {database} SET TIMEZONE TO 'asia/vladivostok';")
            cls.disconnect()
            print('[INFO] Added database into PostgreSQL')
        except (Exception, Error) as error:
            print("[ERROR] Couldn't add database into PostgreSQL\n", error)


    @classmethod
    def connect(cls) -> None:
        try:
            if not cls.__instance:
                cls.__instance = connect(
                    user=user, database=database, password=password, host=host, port=port
                )
                cls.__instance.autocommit = True

                print('[INFO] Connected with PostgreSQL')

        except (Exception, Error) as error:
            print("[ERROR] Conn couldn't connect with PostgreSQL\n", error)


    @classmethod
    def disconnect(cls) -> None:
        if cls.__instance:
            cls.__instance.close()
            cls.__instance = None
            print('[INFO] Disconnected with PostgreSQL')


    @classmethod
    def execute(cls, command: str, args: tuple = ()) -> None:
        try:
            if not cls.__instance:
                cls.connect()

            with cls.__instance.cursor() as cursor:
                cursor.execute(command, args) if args else cursor.execute(command)
                print('[INFO] Conn executed successfully')

        except (Exception, Error) as error:
            print('[ERROR] Exception while Conn is executing\n', error)


    @classmethod
    def execute_many_args(cls, command: str, args: tuple = ()) -> None:
        try:
            if not cls.__instance:
                cls.connect()

            with cls.__instance.cursor() as cursor:
                cursor.executemany(command, args)
                print('[INFO] Conn executed successfully')

        except (Exception, Error) as error:
            print('[ERROR] Exception while Conn is executing\n', error)


    @classmethod
    def execute_many_commands(cls, commands: list[tuple[str, tuple]]) -> None:
        if len(commands) > 0:
            for command, args in commands:
                cls.execute(command, args=args)


    @classmethod
    def select(cls, command: str, args: tuple = ()) -> list[tuple]:
        try:
            if not cls.__instance:
                cls.connect()

            with cls.__instance.cursor() as cursor:
                cursor.execute(command, args) if args else cursor.execute(command)
                print('[INFO] Conn selected successfully')
                return cursor.fetchall()

        except (Exception, Error) as error:
            print('[ERROR] Exception while Conn is selecting\n', error)

    @classmethod
    @property
    def connection(cls):
        return cls.__instance
