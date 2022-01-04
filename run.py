from jobmanager import creat_app

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from jobmanager.functions.add_column import add_columns

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))



if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
    # scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app = creat_app()
    app.run(debug=True)


