from flask_restful import Resource, reqparse, abort
from flask import request, jsonify


def abort_if_task_id_not_exists(task_id):
    if task_id not in tasks:
        abort (404, message='The task does not exists.')

dict_func_description = {
    '1': 'this is first api description',
    'helloworld': 'this is second api description',
    'pm_validation': 'this is a post mile validation function'
}


def abort_if_func_not_exists(func_name):
    if func_name not in dict_func_description:
        abort(404, message='The function does not exists.')


#setup db to persist the task data
#db.column, task_id, input_file_url, task_status, output_file_url

#check task

tasks = {}

pm_put_args = reqparse.RequestParser()
pm_put_args.add_argument('ID', type=int, help='unique ID of the post mile data.')
pm_put_args.add_argument('PMstring', type=str, help='Post mile DynSeg strings.')
pm_put_args.add_argument('Alignment', type=str, help='Roadway Alignment.')

class TaskManager(Resource):
    def post(self, func_name):
        abort_if_func_not_exists(func_name)

        task_id = len(tasks)+1
        args = pm_put_args.parse_args()
        tasks[task_id] = args
        return tasks[task_id], 201

        #save file to local drive with unique name

        #log the task to table

    def get(self,task_id):
        #get from db and return the status of task_id
        return {'status': 'The job is finished' }

class PostMile(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource


    # def get(self, task_id):
    #     # desc = dict_func_description[func_name]
    #     # return jsonify({func_name: desc}
    #
    #     try:
    #         return jsonify({task_id: tasks[task_id]})
    #     except:
    #         return jsonify({'message': 'the requested task id ({}) is not available'.format(task_id)})
    #
    # # Corresponds to Put request
    #
    # def put(self, task_id):
    #     args = pm_put_args.parse_args()
    #     tasks[task_id] = args
    #     return jsonify({tasks[task_id]: args}), 201


    def get(self, task_id):
        # desc = dict_func_description[func_name]
        # return jsonify({func_name: desc}
        abort_if_task_id_not_exists(task_id)
        return tasks[task_id]


    def put(self, task_id):
        args = pm_put_args.parse_args()
        tasks[task_id] = args
        return tasks[task_id], 201