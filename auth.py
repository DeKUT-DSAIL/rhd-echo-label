#from flask import render_template, request, redirect, url_for, session
from flask import request, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import MySQLdb  # Add this import

mysql = MySQL()


def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    hashed_password = generate_password_hash(password)

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                    (username, hashed_password, email))
        mysql.connection.commit()
        cur.close()
        current_app.logger.info(f"User {username} registered successfully")
        return True
    except mysql.connection.IntegrityError as e:
        current_app.logger.error(f"Username already exists: {e}")
        return False
    except Exception as e:
        print(f"Error during registration: {e}")
        mysql.connection.rollback()
        cur.close()
        current_app.logger.error(f"Error during registration: {e}")
        return False
    
def login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            # The password in the database is stored using scrypt, so we need to verify it differently
            from werkzeug.security import check_password_hash
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                current_app.logger.info(f"User {username} logged in successfully")
                return True
        current_app.logger.info(f"Login failed for user {username}")
        return False
    except Exception as e:
        current_app.logger.error(f"Error during login: {str(e)}")
        return False

def logout():
    session.clear()