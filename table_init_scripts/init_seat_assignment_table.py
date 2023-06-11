from utils.db_connector import DBConnector


def init_seat_assignments_table():
    """
    Initializes a Sample Table.
    Important : Version is being used to support optimistic locking.
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS seat_assignments (
        seat_id INT PRIMARY KEY,
        seat_number VARCHAR(10) NOT NULL,
        seat_status ENUM('available', 'booked') NOT NULL DEFAULT 'available',
        version INT,
        user_id INT,
    )
    """

    db_connection = DBConnector().get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute(create_table_query)

    insert_rows_query = """
    INSERT INTO seat_assignments (seat_id, seat_number, seat_status, user_id)
    VALUES
        (1, 'A1', 'available', 1, NULL),
        (2, 'A2', 'available', 1, NULL),
        (3, 'A3', 'booked', 1, 123),
        (5, 'B1', 'booked', 1, 356),
        (6, 'B2', 'booked', 1, 489),
        (7, 'B3', 'available', 1, NULL),
        (8, 'C1', 'available', 1, NULL),
        (9, 'C2', 'available', 1, NULL),
        (10, 'C3', 'available', 1, NULL)
    """

    cursor.execute(insert_rows_query)
    db_connection.commit()
    db_connection.close()


init_seat_assignments_table()
