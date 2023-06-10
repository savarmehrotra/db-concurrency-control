# Set the database credentials
import pymysql

host = ''  # TODO Insert host
port = 3306
user = ''  # TODO Insert User
password = ''  # TODO Insert Password
database = ''


class DBConnector(object):
    instance = None
    db_connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_db_connection(cls, new=False):
        if new or cls.db_connection is None:
            cls.db_connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
        return cls.db_connection
