from utils.db_connector import DBConnector


def assign_seat(user_id, seat_number):
    db_connection = DBConnector().get_db_connection()

    try:
        cursor = db_connection.cursor()

        # Start a transaction and set the isolation level to READ COMMITTED
        cursor.execute("START TRANSACTION")
        cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")

        # Acquire a shared lock on the seat row
        cursor.execute(f"SELECT * FROM seats WHERE seat_number = '{seat_number}' FOR SHARE")
        result = cursor.fetchone()

        if not result:
            print(f"Seat {seat_number} does not exist.")
        elif result[2] == 'booked' or result[2] == 'reserved':
            print(f"Seat {seat_number} is already occupied.")
        else:
            cursor.execute(
                f"UPDATE seats SET seat_status = 'booked', user_id = {user_id} WHERE seat_number = '{seat_number}'")
            db_connection.commit()
            print(f"Seat {seat_number} assigned to User {user_id}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db_connection.rollback()

    finally:
        db_connection.close()


# Accept userID and seat number from CLI
user_id = input("Enter user ID: ")
seat_number = input("Enter seat number: ")
assign_seat(user_id, seat_number)
