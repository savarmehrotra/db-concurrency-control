from utils.db_connector import DBConnector


def display_table(table_name):
    db_connection = DBConnector().get_db_connection()
    cursor = db_connection.cursor()

    select_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_query)

    rows = cursor.fetchall()
    for row in rows:
        for value in row:
            print(value)
        print()

    db_connection.close()
