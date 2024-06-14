from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id= task_id_control, title=data['title'], description=data.get('description',''))
    task_id_control +=1
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso!", "id": new_task.id}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks":task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output), 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = [task for task in tasks if task.id == id]
    if len(task) == 0:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    return jsonify(task[0].to_dict()), 200

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    global tasks
    data = request.get_json()
    task = [task for task in tasks if task.id == id]
    if len(task) == 0:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    task[0].title = data['title']
    task[0].description = data.get('description','')
    task[0].completed = data["completed"]
    return jsonify({"message": "Tarefa atualizada com sucesso!"}), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    task = [task for task in tasks if task.id == id]
    if len(task) == 0:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    tasks.remove(task[0])
    return jsonify({"message": "Tarefa deletada com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)