from utils.db_connector import DBConnector


# TODO : Can be done similarly on a row. While the user is checking out
def display_seats():
    """
    Fetches seat data from the seat_assignments table using FOR SHARE.

    This function acquires a shared lock on the seat rows, allowing other transactions
    to read the seat data but preventing them from modifying it until the lock is released.
    The fetched seat data is then displayed.
    """
    try:
        db_connection = DBConnector().get_db_connection()
        db_connection.start_transaction()
        cursor = db_connection.cursor()

        # Acquire a shared lock on the seat rows
        cursor.execute("SELECT * FROM seat_assignments FOR SHARE")

        # Fetch and display the seat data
        seat_assignments = cursor.fetchall()
        for assignment in seat_assignments:
            print(assignment)

        db_connection.commit()
        cursor.close()
        db_connection.close()

    except Exception as e:
        print("Error occurred:", e)
