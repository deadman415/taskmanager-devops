from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allow React frontend to call this API

# ─── Database Configuration ───────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",         # Change to your MySQL username
    "password": "deadman415",     # Change to your MySQL password
    "database": "taskmanager"
}

def get_db():
    """Create and return a new DB connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ─── Routes ───────────────────────────────────────────────────────────────────

# GET all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(tasks)


# POST a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        (title, description)
    )
    db.commit()
    new_id = cursor.lastrowid
    cursor.close()
    db.close()
    return jsonify({"id": new_id, "message": "Task created"}), 201


# PUT — toggle task status (pending ↔ completed)
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT status FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    new_status = "completed" if task["status"] == "pending" else "pending"
    cursor.execute(
        "UPDATE tasks SET status = %s WHERE id = %s",
        (new_status, task_id)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": f"Status updated to {new_status}"})


# DELETE a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Task deleted"})


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
