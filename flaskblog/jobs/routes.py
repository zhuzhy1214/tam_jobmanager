from datetime import datetime
import time
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, send_file
from flaskblog import db
from flaskblog.jobs.forms import NewJobForm
from flaskblog.models import Job
from flask_login import current_user, login_required
from flaskblog.users.utils import save_file

jobs = Blueprint('jobs', __name__)

now_timestamp = time.time()
utc_offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)


@jobs.route("/jobs/new", methods=['GET', 'POST'])
@login_required
def new_job():
    form = NewJobForm()

    if form.validate_on_submit():

        if form.input_file.data:
            print('saving input file...')
            input_filepath = save_file(form.input_file.data, 'data/input')
        else:
            input_filepath = ''
        # input_filepath = save_file(form.input_file.data, 'data/input')
        # print(input_filepath)
        # print(db.engine.table_names())

        cur_job = Job(
            func_name=form.func_name.data,
            notes=form.notes.data,
            input_path=input_filepath,
            sponsor=current_user
        )
        db.session.add(cur_job)
        db.session.commit()
        flash('Your job has been created', 'success')
        return redirect(url_for('jobs.list_jobs'))
    print('render')
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
        job.input_path = form.input_file.data
        job.date_requested = datetime.utcnow
        db.session.commit()
        flash('The job has been updated!', 'success')

        return redirect(url_for('jobs.list_jobs'))
    elif request.method == 'GET':
        form.notes.data = job.notes
        form.input_file.data = job.input_path
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
    return redirect(url_for('jobs.list_jobs'))


@jobs.route("/job/<int:job_id>/download", methods=['GET'])
@login_required
def download_file(job_id):
    job = Job.query.get_or_404(job_id)
    if job.sponsor != current_user:
        abort(403)
    #to be switched to output_filepath
    input_filepath = job.input_path
    return send_file(input_filepath, as_attachment=True)
