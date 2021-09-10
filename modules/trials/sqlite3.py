import mysql
from mysql.connector import errorcode

'''create a connection that connects to an SQLite database 
specified by the database file rhd_db'''
def create_connection(rhd_db):
    conn = None
    try:
        conn = mysql.connector.connect(rhd_db)
    except mysql.connector.Error as err:
        print("Error")
    finally:
        if conn:
            conn.close

#Takes connection,table for and db_name.
def create_table(conn,TABLES,DB_NAME):
	#create cursor 
    cursor = conn.cursor()
    print('Cursor created')

    #Create table
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist.".format(DB_NAME))  
        else:
            print("Database exists.".format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    conn.close()