import os
from flask import request, Blueprint, abort, jsonify, json, current_app
from flaskblog import db
from flaskblog.models import Job
from werkzeug.utils import secure_filename

rest_api = Blueprint('rest_api', __name__)

ALLOWED_EXTENSIONS = {'csv, xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# dict_func_description = {
#     '1': 'this is first api description',
#     'helloworld': 'this is second api description',
#     'pm-validation': 'this is a post mile validation function'
# }
#
#
# tasks = {}
#
# def abort_if_job_id_not_exists(job_id):
#
#     if job_id not in tasks:
#         abort(404, message='The task does not exists.')

# @rest_api.route("/api", methods=['GET'])
# def sample():
#     return jsonify({'name': 'Jimit',
#                     'address': 'India'})
#
# @rest_api.route('/pm-validate/<string:func>', methods=["POST", 'GET'])
# def pm_validate(func):
#     if func == 'describe':
#         output = dict_func_description['pm-validation']
#     elif func == 'submit' and request.method == "POST":
#         # inputs = request.form['data']
#         inputs = request.get_json()
#         task_id = len(tasks) + 1
#         tasks[task_id] = inputs
#         output = {task_id: inputs}
#     else:
#         output = 'bad request'
#
#     return jsonify(output)


@rest_api.route('/jm/finish/<int:job_id>', methods=['POST'])
def finish_job(job_id):

    #receive a json with:
    # file:file_object, meta{'job_id': 2, 'log':'returned notes for this job'}

    # https://stackoverflow.com/questions/47679227/using-python-to-send-json-and-files-to-flask

    posted_data = json.load(request.files['meta'])
    job_id = posted_data['job_id']
    job = Job.query.get_or_404(job_id)
    if not job:
        abort(404, message='The task does not exists.')

    if posted_data['log']:
        job.log = posted_data['log']

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"response": "missing output file."})
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(output_filepath)
        job.output_path = output_filepath
    else:
        # abort(404, message="wrong file. allowed format: {}".format(ALLOWED_EXTENSIONS))
        return jsonify({"response": "wrong file. allowed format: {}".format(ALLOWED_EXTENSIONS)})

    db.session.commit()
    return jsonify({"response": "success"})

@rest_api.route('/jm/checkout', methods=['GET'])
def checkout_job():
    top_job = Job.query.filter_by(status='Job In Queue') \
        .order_by(Job.date_requested.asc()).first()

    if top_job:
        return jsonify({'id': top_job.id,
                        'file': top_job.input_file
                        })
    else:
        return jsonify({"response": "'No Job In Queue'"})


# @rest_api.route('/jm/list', methods=['GET'])
# def tm_get_task_list():
#     output = {'tasklist': tasks}
#
#     return jsonify(output)