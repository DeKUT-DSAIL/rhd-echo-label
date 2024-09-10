# echo-

# Echo Label

Echo Label  is a web application designed for labeling image and video data. It provides a user-friendly interface for users to log in, view unlabeled files, and assign labels to them.

## Features

- User authentication (registration and login)
- Display of image and video files for labeling
- Label submission and storage in a database
- Automatic progression to the next unlabeled file

## Requirements

To run this web application, you'll need:

1. Python 3.7+
2. Flask
3. Flask-MySQLdb
4. MySQL database

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/echo-labelv1.git
   cd echo-labelv1
   ```

2. Install the required Python packages:
   ```
   pip install Flask Flask-MySQLdb
   ```

3. Set up a MySQL database and update the configuration in `app/app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'your_mysql_host'
   app.config['MYSQL_USER'] = 'your_mysql_user'
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
   app.config['MYSQL_DB'] = 'your_database_name'
   ```

4. Create a folder `app/static/data` and place your image and video files there.

## Running the Application

1. Set the Flask app environment variable:
   ```
   export FLASK_APP=app/app.py
   ```

2. Run the Flask development server:
   ```
   flask run
   ```

3. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Register a new account or log in with existing credentials.
2. You will be presented with unlabeled files one at a time.
3. Enter a label for each file and submit.
4. Continue labeling until all files are processed.

## Note

Ensure that your MySQL server is running and accessible before starting the application. Also, make sure to set appropriate file permissions for the data folder and its contents.
