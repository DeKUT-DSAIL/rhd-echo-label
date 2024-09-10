# Echo Label

Echo Label  is a web application designed for labeling image and video data. It provides a user-friendly interface for users to log in, view unlabeled files, and assign labels to them.

## Features

- User authentication (registration and login)
- Display of image and video files for labeling
- Label submission and storage in a database
- Automatic progression to the next unlabeled file

## Requirements

To run this web application using Docker, you'll need:

1. Docker
2. Docker Compose

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rhd-echo-label.git
   cd rhd-echo-label
   ```

2. Create a `.env` file in the root directory with the following content:
   ```
   MYSQL_ROOT_PASSWORD=your_root_password
   MYSQL_DATABASE=your_database_name
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   ```

3. Create a folder `app/static/data` and place your image and video files there.

## Running the Application

1. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

2. Access the application in your web browser at `http://localhost:5000`.

3. To stop the application, use:
   ```
   docker-compose down
   ```

## Usage

1. Register a new account or log in with existing credentials.
2. You will be presented with unlabeled files one at a time.
3. Enter labels for each file and submit.
4. Continue labeling until all files are processed.

## Note

Ensure that Docker is running on your system before starting the application. The first time you run `docker-compose up`, it may take a few minutes to download and build the necessary images.

## Troubleshooting

If you encounter any issues:

1. Ensure all required ports are free (especially 5000 and 3306).
2. Check Docker logs for any error messages:
   ```
   docker-compose logs
   ```
3. If database connection issues occur, you may need to wait a bit longer for MySQL to fully initialize on the first run.
