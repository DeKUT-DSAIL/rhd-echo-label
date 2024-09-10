from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, send_from_directory
from flask_mysqldb import MySQL
from auth import login, logout, register
from labeling import label_data
import os
from flask import current_app
import json
import logging

app = Flask(__name__)
app.secret_key = 'api'  # for session management

app.secret_key = os.environ.get('SECRET_KEY', 'api')

# Configure logging
logging.basicConfig(level=logging.INFO)


# MySQL configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'rhd_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['DATA_FOLDER'] = os.path.join(app.root_path, 'static', 'data')

list_of_views = ['Parasternal long axis (PLAX)', 'Parasternal short axis(PSAX)', 'Apical Four Chamber(A4C)', 'Apical three chamber (A3C)', 'Apical two chamber(A2C)', 'Suprasternal(SSN)', 'Subcostal', 'Doppler']
list_of_colours = ['Colour', 'No Colour']
list_of_thickness_state = ['Thick', 'Not Thick', 'Not Applicable']
list_of_conditions = ['Mitral Valve Regurgitation', 'Aortic Valve Regurgitation', 'Tricuspid Valve Regurgitation', 'Pulmonary Valve Regurgitation', 'Aortic Valve Stenosis', 'Mitral Valve Stenosis', 'Tricuspid Valve Stenosis', 'Pulmonary Valve Stenosis', 'Mitral Valve Prolapse', 'Not Applicable']
list_of_severities = ['Normal', 'Borderline rhd', 'Definite rhd', 'Not Applicable']


mysql = MySQL(app)

def create_users_table():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        )
        """)
        mysql.connection.commit()
        cur.close()
        app.logger.info("Users table created or already exists")
    except Exception as e:
        app.logger.error(f"Error creating users table: {e}")


def create_labeled_data_table():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS labeled_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            view VARCHAR(255) NOT NULL,
            colour VARCHAR(255) NOT NULL,
            thickness_state VARCHAR(255) NOT NULL,
            thickness_comment VARCHAR(255) NULL,
            conditions VARCHAR(255) NOT NULL,
            conditions_comment VARCHAR(255) NULL,
            echo_quality_comment VARCHAR(255) NULL,
            severity VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            username VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        mysql.connection.commit()
        cur.close()
        app.logger.info("Labeled data table created or already exists")
    except Exception as e:
        app.logger.error(f"Error creating labeled data table: {e}")

# Call create_users_table after the app context is created
with app.app_context():
    create_users_table()
    create_labeled_data_table()


def get_file_type(filename):
    lower_filename = filename.lower()
    if lower_filename.endswith(('.mp4', '.avi', '.mov', '.webm')):
        return 'video'
    elif lower_filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return 'image'
    else:
        return 'unknown'
    
def get_next_file_to_label():
    data_folder = current_app.config['DATA_FOLDER']
    labeled_files = set()
    
    # Get all labeled files from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT filename FROM labeled_data")
    for row in cur.fetchall():
        labeled_files.add(row['filename'])
    cur.close()
    
    # Find the first unlabeled file in the data folder
    for filename in os.listdir(data_folder):
        if filename not in labeled_files and (filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.avi', '.mov'))):
            return filename
    
    return None  # Return None if all files are labeled


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())
    app.logger.info('Session: %s', session)

@app.route('/static/data/<path:filename>')
def serve_video(filename):
    return send_from_directory(app.config['DATA_FOLDER'], filename, mimetype='video/mp4')

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('label_route'))
    return redirect(url_for('login_route'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    app.logger.info(f"Current session: {session}")
    if 'user_id' in session:
        app.logger.info(f"User already logged in, redirecting to label route")
        return redirect(url_for('label_route'))
    
    if request.method == 'POST':
        app.logger.info("Login attempt")
        if login():
            app.logger.info(f"Login successful for user {session.get('username')}")
            app.logger.info(f"Session after login: {session}")
            return redirect(url_for('label_route'))
        else:
            app.logger.info("Login failed")
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        app.logger.info(f"Registration attempt with username: {request.form.get('username')}")
        if register():
            flash('Registration successful. Please log in.')
            return redirect(url_for('login_route'))
        else:
            flash('Registration failed. Please try again.')
    return render_template('register.html')


# @app.route('/start_labeling')
# def start_labeling():
#     if 'user_id' not in session:
#         return redirect(url_for('login_route'))
#     session['labeled_files'] = 0  # Initialize here
#     return redirect(url_for('label_route'))

@app.route('/label', methods=['GET', 'POST'])
def label_route():
    app.logger.info(f"Accessing label route. Current session: {session}")
    if 'user_id' not in session:
        app.logger.info("User not logged in, redirecting to login")
        return redirect(url_for('login_route'))
    
    total_files = len([f for f in os.listdir(app.config['DATA_FOLDER']) if os.path.isfile(os.path.join(app.config['DATA_FOLDER'], f))])
    

     # Initialize or adjust labeled_files count
    if 'labeled_files' not in session or session['labeled_files'] > total_files:
        session['labeled_files'] = 0
    
    current_file_index = session['labeled_files']


    if request.method == 'POST':
        filename = request.form.get('filename')
        view = request.form.get('view')
        colour = request.form.get('colour')
        thickness_state = request.form.get('thickness_state')
        thickness_comment = request.form.get('thickness_comment')
        conditions = request.form.getlist('conditions')
        conditions_comment = request.form.get('conditions_comment')
        echo_quality_comment = request.form.get('echo_quality_comment')
        severity = request.form.get('severity')
        user_id = session['user_id']
        username = session['username']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO labeled_data (filename, view, colour, thickness_state, thickness_comment, conditions, conditions_comment, echo_quality_comment, severity, user_id, username)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                view = VALUES(view),
                        colour = VALUES(colour), 
                         thickness_state = VALUES(thickness_state), 
                        thickness_comment = VALUES(thickness_comment),
                         conditions = VALUES(conditions), 
                        conditions_comment = VALUES(conditions_comment), 
                        echo_quality_comment = VALUES(echo_quality_comment), 
                        severity = VALUES(severity), 
                        user_id = VALUES(user_id), 
                        username = VALUES(username)
            """, (filename,view,  colour,  thickness_state, thickness_comment, conditions, conditions_comment, echo_quality_comment, severity, user_id, username))
            mysql.connection.commit()
            cur.close()
            flash('Data labeled successfully!')
            session['labeled_files'] = min(session['labeled_files'] + 1, total_files)
            current_file_index = session['labeled_files']
        except Exception as e:
            app.logger.error(f"Error saving labeled data: {e}")
            flash(f'Error saving labeled data: {str(e)}. Please try again.')
    
    file_to_label = get_next_file_to_label()
    if file_to_label is None:
        flash('All files have been labeled!')
        return render_template('label.html', username=session.get('username'), 
                               file_to_label=None,
                               current_file_index=total_files,  # Set to total_files when all are labeled
                              total_files=total_files,
                              list_of_views=list_of_views,
                              list_of_colours=list_of_colours,
                              list_of_thickness_state=list_of_thickness_state,
                              list_of_conditions=list_of_conditions,
                              list_of_severities=list_of_severities
                              )
    
    file_type = 'video' if file_to_label.lower().endswith(('.mp4', '.avi', '.mov')) else 'image'
    
    
    # Adjust current_file_index to include the file currently being viewed
    current_file_index = min(current_file_index + 1, total_files)
    app.logger.info(f"User {session.get('username')} logged in, proceeding to label page")
    return render_template('label.html', 
                           username=session.get('username'), 
                           file_to_label=file_to_label, 
                           file_type=file_type,
                           current_file_index=current_file_index,
                           total_files=total_files,
                              list_of_views=list_of_views,
                           list_of_colours=list_of_colours,
                              list_of_thickness_state=list_of_thickness_state,
                              list_of_conditions=list_of_conditions,
                              list_of_severities=list_of_severities
                              )


@app.route('/test_db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        cur.close()
        return f"Database connection successful. Tables: {tables}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    current_file_index = data.get('current_file_index')
    total_files = data.get('total_files')
    # Process the data as needed
    print(f'Current File Index: {current_file_index}, Total Files: {total_files}')
    return jsonify({'status': 'success'})


# @app.route('/clear_labels', methods=['GET', 'POST'])
# def clear_labels():
#     if 'user_id' not in session:
#         flash('You must be logged in to clear labels.')
#         return redirect(url_for('login_route'))
    
# @app.route('/clear_labels', methods=['GET', 'POST'])
# def clear_labels():
#     if request.method == 'POST':
#         try:
#             cur = mysql.connection.cursor()
#             cur.execute("TRUNCATE TABLE labeled_data")
#             mysql.connection.commit()
#             cur.close()
#             flash('All labels have been cleared successfully!')
#         except Exception as e:
#             app.logger.error(f"Error clearing labeled data: {e}")
#             flash(f'Error clearing labeled data: {str(e)}')
#         return redirect(url_for('home'))
    
#     return render_template('clear_labels.html')
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout')
def logout_route():
    logout()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)