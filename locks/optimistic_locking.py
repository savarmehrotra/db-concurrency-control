from utils.db_connector import DBConnector


def assign_seat_optimistic(user_id, seat_number):
    db_connection = DBConnector().get_db_connection()
    cursor = db_connection.cursor()

    try:
        cursor.execute("START TRANSACTION")
        cursor.execute(f"SELECT seat_status, current_version FROM seats WHERE seat_number = %s", (seat_number,))
        result = cursor.fetchone()

        if not result:
            print(f"Seat {seat_number} does not exist.")
        elif result[0] == 'booked':
            print(f"Seat {seat_number} is already occupied.")
        else:
            current_version = result[1]

            # Update the seat status and increment the version
            updated_status = 'booked'
            updated_version = current_version + 1

            # TODO : Read this query carefully. Also, during the actual update, the DB is taking a lock by default.
            cursor.execute("UPDATE seats SET seat_status = %s, version = %s WHERE seat_number = %s AND version = %s",
                           (updated_status, updated_version, seat_number, current_version))

            affected_rows = cursor.rowcount

            if affected_rows == 0:
                print("Failed to assign the seat. Another transaction may have modified the seat.")
                db_connection.rollback()
            else:
                db_connection.commit()
                print(f"Seat {seat_number} assigned to User {user_id}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db_connection.rollback()

    finally:
        db_connection.close()


# Accept user input for user ID and seat number
user_id = input("Enter user ID: ")
seat_number = input("Enter seat number: ")
assign_seat_optimistic(user_id, seat_number)
