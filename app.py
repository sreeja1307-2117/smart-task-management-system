import pandas as pd
import numpy as np
from flask_socketio import SocketIO
from flask import Flask, render_template,request,jsonify,redirect
import mysql.connector
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "WJ28@krhps",
    database = "task_manager"
)
cursor = conn.cursor()
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        
        password = request.form["password"]

        return f"Welcome {username}"
    return render_template("login.html")


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        query = "INSERT INTO users(username,password) VALUES(%s,%s)"

        values = (username,password)

        cursor.execute(query,values)

        conn.commit()

        return "User Registered Successfully"
    
    return render_template("register.html")

@app.route('/add_task', methods=["GET","POST"])
def add_task():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]

        query = """INSERT INTO tasks(title,description,priority,status)
        VALUES (%s,%s,%s,%s)"""

        values = (title,description,priority,status)

        cursor.execute(query, values)
        conn.commit()
        socketio.emit("task_update", {"message": "New task added"})

        return "Task Added Successfully"
    return render_template("add_task.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    tasks = cursor.fetchall()
    return jsonify(tasks)

@app.route("/view_tasks")
def view_tasks():
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    tasks = cursor.fetchall()
    print(tasks)
    return render_template("view_tasks.html", tasks=tasks)


@app.route("/delete_task/<int:id>")
def delete_task(id):
    query = "DELETE FROM tasks WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    conn.commit()
    return redirect("/view_tasks")

@app.route("/update_task/<int:id>", methods=["GET","POST"])
def update_task(id):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]

        query = """UPDATE tasks SET title=%s, description=%s, priority=%s, status=%s WHERE id=%s"""
        values = (title, description, priority, status, id)
        cursor.execute(query, values)
        conn.commit()
        return redirect("/view_tasks")
    
    query = "SELECT * FROM tasks WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    task = cursor.fetchone()
    return render_template("update_task.html", task=task)

@app.route("/analytics")
def analytics():

    query = "SELECT * FROM tasks"
    cursor.execute(query)
    tasks = cursor.fetchall()
    df = pd.DataFrame(tasks, columns=
                      ["id", "title", "description", "priority", "status","created_date"])
    
    total_tasks = len(df)
    completed_tasks = len(df[df["status"] == "Completed"])  
    pending_tasks = len(df[df["status"] == "Pending"])  

    if total_tasks>0:

        completion_percentage = (
            completed_tasks / total_tasks) * 100
        
    else:
        completion_percentage = 0

    return render_template("analytics.html",
                            total_tasks=total_tasks,
                            completed_tasks=completed_tasks,
                            pending_tasks=pending_tasks,
                            completion_percentage=round(completion_percentage, 2))

if __name__ == '__main__':
    socketio.run(app, debug=True)
