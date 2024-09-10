from flask import current_app, session
import mysql.connector
import json
from mysql.connector import Error


            
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        return connection
    except Error as e:
        raise Exception(f"Error connecting to MySQL database: {e}")




def save_labels(file_path, labels):
    try:
        connection = get_db_connection()  # Implement this function to get your database connection
        cursor = connection.cursor()

        query = """
        INSERT INTO labeled_data 
        (file_path, view, colour, thickness_state, thickness_comment, conditions, conditions_comment, echo_quality_comment, severity, timetaken, labeled_by) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        view = VALUES(view), colour = VALUES(colour), thickness_state = VALUES(thickness_state),
        thickness_comment = VALUES(thickness_comment), conditions = VALUES(conditions),
        conditions_comment = VALUES(conditions_comment), echo_quality_comment = VALUES(echo_quality_comment),
        severity = VALUES(severity), timetaken = VALUES(timetaken), labeled_by = VALUES(labeled_by)
        """

        values = (
            file_path,
            labels['view'],
            labels['colour'],
            labels['thickness_state'],
            labels['thickness_comment'],
            labels['conditions'],  # This is now a JSON string
            labels['conditions_comment'],
            labels['echo_quality_comment'],
            labels['severity'],
            labels['timetaken'],
            session.get('username', 'unknown')  # Get username from session, default to 'unknown' if not found
        )

        cursor.execute(query, values)
        connection.commit()

    except Error as e:
        raise Exception(f"Database error: {str(e)}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_next_unlabeled_file():
    # Query database to find next unlabeled file
    # Return file path
    pass