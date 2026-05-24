# Smart Task Management System

A Flask-based web application for managing tasks with authentication, analytics, and real-time notifications.

---

## Features

- User Registration
- User Login
- Add Tasks
- View Tasks
- Update Tasks
- Delete Tasks
- Task Analytics
- Real-time Notifications using WebSockets

---

## Technologies Used

- Python
- Flask
- MySQL
- Pandas
- NumPy
- HTML
- CSS
- Flask-SocketIO

---

## Project Structure

smart-task-manager/
│
├── app.py
├── templates/
├── static/
├── README.md

---

## Installation

1. Install Python
2. Install required libraries

```bash
pip install flask mysql-connector-python pandas numpy flask-socketio 

3.Create MySQL database
CREATE DATABASE task_manager;

4.Run Flask Application
python app.py