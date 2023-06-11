from display_table import display_table
from utils.db_connector import DBConnector


def reserve_seat(seat_id, user_id):
    # Get the database connection and cursor
    db_connection = DBConnector().get_db_connection()
    cursor = db_connection.cursor()

    try:
        # Start a transaction
        db_connection.start_transaction()

        # Acquire a shared lock on the seat
        cursor.execute("SELECT * FROM assignments_optimistic WHERE seat_id = %s FOR SHARE", (seat_id,))
        seat_data = cursor.fetchone()

        if seat_data is None:
            print("Seat not found.")
            return

        seat_status = seat_data[2]

        if seat_status == 'booked':
            print("Seat is already booked.")
            return

        # Acquire an exclusive lock on the seat
        cursor.execute("SELECT * FROM assignments_optimistic WHERE seat_id = %s FOR UPDATE", (seat_id,))
        seat_data = cursor.fetchone()

        if seat_data is None:
            print("Seat not found.")
            return

        seat_status = seat_data[2]

        if seat_status == 'booked':
            print("Seat is already booked.")
            return

        # Update the seat status and user ID
        cursor.execute("UPDATE assignments_optimistic SET seat_status = 'booked', user_id = %s WHERE seat_id = %s",
                       (user_id, seat_id))

        # Commit the transaction
        db_connection.commit()

    except mysql.connector.Error as error:
        # Rollback the transaction in case of any error
        db_connection.rollback()
        print("Error occurred:", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        db_connection.close()


# Initialize the table
init_optimistic_locking_seat_assignment_table()

# Reserve seat with ID 1 for user 100
reserve_seat(1, 100)
