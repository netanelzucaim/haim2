# SuperFastPython.com
# example of joining a thread with a timeout
from time import sleep
from threading import Thread
import os
# target function
def task():
    # block for a moment
    sleep(20)
    # report a message
    print('All done in the new thread')
def print_ids(thread):
    thread_id = thread.ident  # Get thread ID
    process_id = os.getpid()  # Get process ID
    print(f"Thread ID: {thread_id}, Process ID: {process_id}") 
# create a new thread
thread = Thread(target=task)
# start the new thread
thread.start()
print_ids(thread)
# wait for the new thread to finish
print('Main: Waiting for thread to terminate...')
thread.join(timeout=6)
print_ids(thread)
# check if the thread is still alive
if thread.is_alive():
    print('Main: The target thread is still running')
else:
    print('Main: The target thread has terminated')