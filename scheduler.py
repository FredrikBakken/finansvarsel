import queue
import time
import threading
import schedule

from main import finance_controller
from main import user_controller
from main import notification_controller


jobqueue = queue.Queue()


def queue_worker():
    while 1:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()


def thread_scheduler():
    schedule.every().day.at("02:00").do(finance_controller)
    schedule.every().friday.at("21:00").do(notification_controller)

    worker_thread = threading.Thread(target=queue_worker)
    worker_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(30)
        user_controller()
