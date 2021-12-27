import os
from flask import request, Blueprint, abort, jsonify, json, current_app, send_from_directory
from flaskblog import db
from flaskblog.models import Job
from werkzeug.utils import secure_filename
from flaskblog.utils.util_func import save_file

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager


rest_api = Blueprint('rest_api', __name__)

ALLOWED_EXTENSIONS = {'csv, xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#
#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401
#
#         try:
#             data = jwt.decode(token, current_app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated

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
#
# @rest_api.route('/jm/finish/<int:job_id>', methods=['POST'])
# def new_job(job_id):
#     #TODO use AUTH0 to sub user credential
#
#
#     posted_data = json.load(request.files['meta'])
#     func_name = posted_data['func_name']
#     notes = posted_data['notes']
#     input_file = posted_data['func_name']
#
#     if 'file' not in request.files:
#         input_file = 'no input file uploaded.'
#     else:
#         #TODO: check if the file type is allowed.
#
#         file = request.files['file']
#         #upload file and get file_name
#         filename = secure_filename(file.filename)
#         input_filepath = os.path.join(current_app.config['INPUTFILE_FOLDER'], filename)
#         file.save(input_filepath)
#
#     cur_job = Job(
#         func_name=posted_data['func_name'],
#         notes=posted_data['notes'],
#         input_file = filename,
#         sponsor=current_user
#     )
#     db.session.add(cur_job)
#     db.session.commit()
#     return ''

@rest_api.route('/api/finish_job', methods=['POST'])
@jwt_required()
def finish_job():
    #receive a json with:
    # file:file_object, meta{'job_id': 2, 'log':'returned notes for this job'}

    # https://stackoverflow.com/questions/47679227/using-python-to-send-json-and-files-to-flask

    job_id = request.args.get("job_id")
    job = Job.query.get_or_404(job_id)
    log = request.args.get("log")
    if log:
        job.log = log

    # check if the post request has the file part
    if 'upload_file' not in request.files:
        return jsonify({"response": "missing output file."})
    file = request.files['upload_file']

    if file:
        file_name = secure_filename(file.filename)
        output_filepath = current_app.root_path+'/'+current_app.config['OUTPUTFILE_FOLDER']
        file_name = save_file(file, output_filepath)
        job.output_file = file_name

    else:
        # abort(404, message="wrong file. allowed format: {}".format(ALLOWED_EXTENSIONS))
        return jsonify({"response": "no file uploaded or wrong file. allowed format: {}".format(ALLOWED_EXTENSIONS)})

    job.status = 'Completed'
    try:
        db.session.commit()
        return jsonify({"response": "success"})
    except:
        return jsonify({"response": "error in writing to db."})


# https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/


@rest_api.route("/api/get_token", methods=["POST"])
def get_token():
    username = request.args.get("username")
    password = request.args.get("password")

    if username != "worker" or password != "pwd":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@rest_api.route("/api/checkout_job", methods=["GET"])
@jwt_required()
def checkout_job():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    func_name = request.args.get('func_name')
    top_job = Job.query.filter_by(status='Job In Queue', func_name=func_name) \
        .order_by(Job.date_requested.asc()).first()

    if top_job:
        return jsonify(response="Job Found", logged_in_as=current_user,
                       func_name=func_name,
                       job_id=top_job.id,
                       notes=top_job.notes,
                       input_file=top_job.input_file), 200
    else:
        return jsonify({"response": "No Job In Queue"})



import mimetypes
@rest_api.route("/api/download_file", methods=["GET"])
@jwt_required()
def download_file():

    fn = request.args.get('file_name')
    file_type = request.args.get('file_type')

    #to be switched to output_filepath

    if file_type == 'input':
        file_path = current_app.root_path+'/'+current_app.config['INPUTFILE_FOLDER']

    elif file_type == 'output':
        file_path = current_app.root_path+'/'+current_app.config['OUTPUTFILE_FOLDER']
    else:
        abort(404, 'You can only request for input or output file.')

    return send_from_directory(file_path, fn, as_attachment=True)
