import queue
import time
import threading
import schedule

from main import finance_controller
from main import user_controller
from main import notification_controller


# Job queue
jobqueue = queue.Queue()

# Creating a queue for scheduled tasks to be executed
def queue_worker():
    while 1:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()


# Method for scheduling tasks
def thread_scheduler():
    # Do this once
    finance_controller()

    # Schedule these tasks
    schedule.every().day.at("02:00").do(finance_controller)
    schedule.every().friday.at("21:00").do(notification_controller)
    #TODO schedule.every().tuesday.at("00:00").do(user_update_notifier)

    # Start threading
    worker_thread = threading.Thread(target=queue_worker)
    worker_thread.start()

    # Loop forever scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(30)
        user_controller()
