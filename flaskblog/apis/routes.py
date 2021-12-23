from flask import request, Blueprint, abort
from flask import jsonify

rest_api = Blueprint('rest_api', __name__)

tasks = {}

def abort_if_task_id_not_exists(task_id):
    if task_id not in tasks:
        abort(404, message='The task does not exists.')

@rest_api.route("/api", methods=['GET'])
def sample():
    return jsonify({'name': 'Jimit',
                    'address': 'India'})

@rest_api.route('/pm-validate/<string:func>', methods=["POST", 'GET'])
def pm_validate(func):
    if func == 'describe':
        output = 'function description'
    elif func == 'submit' and request.method == "POST":
        # inputs = request.form['data']
        inputs = request.get_json()
        task_id = len(tasks) + 1
        tasks[task_id] = inputs
        output = {task_id: inputs}
    else:
        output = 'bad request'

    return jsonify(output)


@rest_api.route('/taskmanager/<int:task_id>', methods=['GET'])
def tm_ck_task_status(task_id):
    if func == 'describe':
        output = 'function description'
    elif func == 'submit' and request.method == "POST":
        inputs = request.get_json(force=True)
        task_id = len(tasks) + 1
        tasks[task_id] = inputs
        output = {task_id: inputs}
    else:
        output = 'bad request'

    return jsonify(output)

@rest_api.route('/taskmanager', methods=['GET'])
def tm_get_task_list():
    output = {'tasklist': tasks}

    return jsonify(output)