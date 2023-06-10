from utils.db_connector import DBConnector


def init_seat_assignment_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS seats (
        seat_id INT PRIMARY KEY,
        seat_number VARCHAR(10) NOT NULL,
        seat_status ENUM('available', 'booked') NOT NULL DEFAULT 'available',
        user_id INT,
    )
    """

    db_connection = DBConnector().get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute(create_table_query)

    insert_rows_query = """
    INSERT INTO seats (seat_id, seat_number, seat_status, user_id)
    VALUES
        (1, 'A1', 'available', NULL),
        (2, 'A2', 'available', NULL),
        (3, 'A3', 'booked', 123),
        (5, 'B1', 'booked', 356),
        (6, 'B2', 'booked', 489),
        (7, 'B3', 'available', NULL),
        (8, 'C1', 'available', NULL),
        (9, 'C2', 'available', NULL),
        (10, 'C3', 'available', NULL)
    """

    # Execute the insert rows query
    cursor.execute(insert_rows_query)

    # Commit the changes and close the database connection
    db_connection.commit()
    db_connection.close()


# Create the table and insert sample rows.
init_seat_assignment_table()
