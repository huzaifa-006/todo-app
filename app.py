from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")

# In-memory storage for tasks
tasks = []

@app.route('/')
def home():
    return send_from_directory("static", "index.html")

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title", "Untitled Task"),
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
