
from datetime import datetime, timedelta
import os
import secrets
from jobmanager.models import Job
from jobmanager import db

#mark jobs that is checked out more than one day




# def utc2local_offset():
#     epoch = time.mktime(utc.timetuple())
#     offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
#     return offset


def save_file(file, folder):
    # create a random file name
    random_hex = secrets.token_hex(4)
    f_n, f_ext = os.path.splitext(file.filename)
    file_name = '{}_{}{}'.format(f_n, random_hex, f_ext)
    file_path = os.path.join(folder, file_name)
    file.save(file_path)
    return file_name

def mark_expired_job():
    print('Mark all jobs that are checked out for more than 24 hours...')
    expired_jobs = Job.query.filter(status='Calculation In Process')\
        .order_by(Job.date_requested.asc())
    # print(len(expired_jobs))
    #
    # # .filter(date_updated < (datetime.utcnow - timedelta(days=1)))\
    #
    # try:
    #     for expired_job in expired_jobs.items:
    #         expired_job.status = 'Job Timed Out'
    #         expired_job.log = 'This job was not finished within 24 hour processing window. Please double check the input and resubmit'
    #         print(expired_job.id)
    #     db.session.commit()
    # except:
    #     return False
    # return True