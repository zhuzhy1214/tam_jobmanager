import os
import datetime
from datetime import timedelta
from flask import request, Blueprint, abort, jsonify, json, current_app, send_from_directory
from jobmanager import db
from jobmanager.models import Job
from werkzeug.utils import secure_filename
from jobmanager.utils.util_func import save_file

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager


rest_api = Blueprint('rest_api', __name__)

ALLOWED_EXTENSIONS = {'csv, xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/


@rest_api.route("/api/get_token", methods=["POST"])
def get_token():
    username = request.args.get("username")
    password = request.args.get("password")

    if username != "worker" or password != "pwd":
        return jsonify({"msg": "Bad username or password"}), 401
    # access_token = create_access_token(identity=username)
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=30))
    return jsonify(access_token=access_token)


@rest_api.route("/api/search_job", methods=["GET"])
@jwt_required()
def search_job():
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
        return jsonify({"response": "No Job In Queue"}), 404

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


@rest_api.route("/api/upload_file", methods=["POST"])
@jwt_required()
def upload_file():
    # check if the post request has the file part
    if 'upload_file' not in request.files:
        return jsonify({"response": "the file is missing."})
    file = request.files['upload_file']

    if file:
        output_folder = current_app.root_path+'/'+current_app.config['OUTPUTFILE_FOLDER']
        file_name = save_file(file, output_folder)

        return jsonify({"response": "file uploaded.",
                        'file_name': file_name
                        })

    else:
        # abort(404, message="wrong file. allowed format: {}".format(ALLOWED_EXTENSIONS))
        return jsonify({"response": "no file uploaded or wrong file. allowed format: {}".format(ALLOWED_EXTENSIONS)})


@rest_api.route('/api/update_job', methods=['POST'])
@jwt_required()
def update_job():
    #receive a json with:
    # file:file_object, meta{'job_id': 2, 'log':'returned notes for this job'}

    # https://stackoverflow.com/questions/47679227/using-python-to-send-json-and-files-to-flask

    job_id = request.args.get("job_id")
    job = Job.query.get_or_404(job_id)

    job_status = request.args.get("job_status")
    if not job_status:
        return jsonify({"response": "no job status information"})
    elif job_status == 'Completed':
        output_file = request.args.get("job_output_file")
        if output_file:
            job.output_file = output_file

    job.status = job_status

    job_log = request.args.get("job_log")
    if job_log:
        job.log = job_log

    job_log = request.args.get("job_log")
    if job_log:
        job.log = job_log

    try:
        db.session.commit()
        return jsonify({"response": "Job Information Updated"}), 200
    except:
        return jsonify({"response": "error in writing to db."})


