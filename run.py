from jobmanager import creat_app
from jobmanager.utils.util_func import mark_expired_job

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler



if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    # scheduler.add_job(func=mark_expired_job, trigger="interval", seconds=60)
    # scheduler.add_job(func=mark_expired_job, trigger="interval", seconds=600)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app = creat_app()
    app.run(debug=True)


