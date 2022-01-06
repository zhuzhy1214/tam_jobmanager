from datetime import datetime
import time
import os
from flask import (render_template, url_for, flash, redirect, request,
                   abort, Blueprint,  current_app, send_from_directory)
from jobmanager import db
from jobmanager.jobs.forms import NewJobForm
from jobmanager.models import Job
from flask_login import current_user, login_required
from jobmanager.utils.util_func import save_file

jobs = Blueprint('jobs', __name__)

now_timestamp = time.time()
utc_offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)

@jobs.route("/jobs/new", methods=['GET', 'POST'])
@login_required
def new_job():
    form = NewJobForm()

    if form.validate_on_submit():

        if form.input_file.data:
            target_folder = current_app.root_path+'/'+current_app.config['INPUTFILE_FOLDER']
            input_file = save_file(form.input_file.data, target_folder)
        else:
            input_file = 'No input file uploaded.'

        cur_job = Job(
            func_name=form.func_name.data,
            notes=form.notes.data,
            input_file=input_file,
            sponsor=current_user
        )
        db.session.add(cur_job)
        db.session.commit()
        flash('Your job has been created', 'success')
        return redirect(url_for('jobs.list_jobs'))

    return render_template('create_job.html', title='Submit New Job',
                           form=form, legend='Submit New Job'
                           )

@jobs.route("/jobs/list", methods=['GET'])
@login_required
def list_jobs():
    # query needs to filter by current_user
    page = request.args.get('page', 1, type=int)
    all_jobs = Job.query.filter_by(sponsor=current_user) \
        .order_by(Job.date_requested.desc()).paginate(page=page, per_page=5)
    return render_template('list_jobs.html', jobs=all_jobs, utc_offset=utc_offset)

@jobs.route("/job/<int:job_id>/update", methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.sponsor != current_user:
        abort(403)
    form = NewJobForm()
    if form.validate_on_submit():
        job.notes = form.notes.data
        job.input_file = form.input_file.data
        job.date_requested = datetime.utcnow
        db.session.commit()
        flash('The job has been updated!', 'success')

        return redirect(url_for('jobs.list_jobs'))
    elif request.method == 'GET':
        form.notes.data = job.notes
        form.input_file.data = job.input_file
    return render_template('update_job.html', title='Update Job',
                           legend='Update Job', job=job, utc_offset=utc_offset
                           )


@jobs.route("/job/<int:job_id>/cancel", methods=['GET', 'POST'])
@login_required
def cancel_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.sponsor != current_user:
        abort(403)
    job.status = 'Job Canceled'
    db.session.commit()
    flash('The job has been canceled!', 'success')
    return redirect(url_for('jobs.update_job', job_id=job_id))


import mimetypes
@jobs.route("/job/<int:job_id>/<string:file_type>/download", methods=['GET'])
@login_required
def download_file(job_id, file_type):
    job = Job.query.get_or_404(job_id)
    if job.sponsor != current_user:
        abort(403)
    #to be switched to output_filepath

    if file_type == 'input':
        file_path = current_app.root_path+'/'+current_app.config['INPUTFILE_FOLDER']
        fn = job.input_file

    elif file_type == 'output':
        file_path = current_app.root_path+'/'+current_app.config['OUTPUTFILE_FOLDER']
        fn = job.output_file

    else:
        abort(404, 'You can only request for input or output file.')

    return send_from_directory(file_path, fn, as_attachment=True)
    # return send_file(file_path, as_attachment=True, mimetype=mime_type)


def mark_elapsed_job():
    print('Mark all jobs that are checked out for more than 24 hours...')
