'''
SMWinservice
by Davide Mastromatteo

Base class to create winservice in Python
-----------------------------------------

Instructions:

1. Just create a new class that inherits from this base class
2. Define into the new class the variables
   _svc_name_ = "nameOfWinservice"
   _svc_display_name_ = "name of the Winservice that will be displayed in scm"
   _svc_description_ = "description of the Winservice that will be displayed in scm"
3. Override the three main methods:
    def start(self) : if you need to do something at the service initialization.
                      A good idea is to put here the inizialization of the running condition
    def stop(self)  : if you need to do something just before the service is stopped.
                      A good idea is to put here the invalidation of the running condition
    def main(self)  : your actual run loop. Just create a loop based on your running condition
4. Define the entry point of your module calling the method "parse_command_line" of the new class
5. Enjoy
'''
from time import sleep
import os
import socket
import time
import threading
import win32serviceutil

import servicemanager
import win32event
import win32service
import win32api
import win32process
import psutil

def get_current_process_info():
    try:
        # Get current process ID
        current_process = psutil.Process()
        current_pid = current_process.pid
        l.info(f"Current Process ID (PID): {current_pid}")

        # Get all threads within the current process
        thread_ids = current_process.threads()
        l.info(f"Thread IDs in Process {current_pid}: {[t.id for t in thread_ids]}")

        # Optionally, return the PID and thread IDs as a tuple
        return current_pid, [t.id for t in thread_ids]

    except Exception as e:
        print(f"Error occurred: {str(e)}")



def print_ids(thread):
    thread_id = thread.ident  # Get thread ID
    print(f"Thread ID: {thread_id}") 
# set up logging #####################################
import sys,logging,logging.handlers,os.path
#in this particular case, argv[0] is likely pythonservice.exe deep in python's lib\
# so it makes no sense to write log there
log_file=os.path.splitext(__file__)[0]+".log"
l = logging.getLogger()
l.setLevel(logging.INFO)
f = logging.Formatter('%(asctime)s %(process)d:%(thread)d %(name)s %(levelname)-8s %(message)s')
h=logging.StreamHandler(sys.stdout)
h.setLevel(logging.NOTSET)
h.setFormatter(f)
l.addHandler(h)
h=logging.handlers.RotatingFileHandler(log_file,maxBytes=1024**2,backupCount=1)
h.setLevel(logging.NOTSET)
h.setFormatter(f)
l.addHandler(h)
del h,f
#hook to log unhandled exceptions
def excepthook(type,value,traceback):
    logging.error("Unhandled exception occured",exc_info=(type,value,traceback))
    #Don't need another copy of traceback on stderr
    if old_excepthook!=sys.__excepthook__:
        old_excepthook(type,value,traceback)
old_excepthook = sys.excepthook
sys.excepthook = excepthook
del log_file,os
#from logger_setup import setup_logger

class WorkerThread(threading.Thread):
    def __init__(self, controller):
        self._controller = controller
        #self._stop = threading.Event()
        super(WorkerThread, self).__init__()

    # def stop(self):
    #     self._stop.set()

    # def stopped(self):
    #     return self._stop.isSet()

    def run(self):
        
           # Insert the code you want to run as a service here
           # rather than do "execfile(.../.../blah)" simply do:
           # You can have your code throw InterruptedException if your code needs to exit
           # Also check often if self.stopped and then cleanly exit
           l.info("Start to sleep")
           sleep(5)

           # if code in another module is not yours or cannot check often if it should stop then use multiprocessing which will spawn separate processes that you can terminate then from here when you need to stop and return
           # in that case simply block here on self._stop.wait()
           l.info("finish to sleep")
           win32event.SetEvent(self._controller)



class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)


    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        l.info("Stop request received")
        self.stop()
        l.info("after Stop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        l.info("after report")
        win32event.SetEvent(self.hWaitStop)
        l.info("after waitstop")

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)      
        self.hWaitDone = win32event.CreateEvent(None, 0, 0, None)
        
    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''

        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        worker = WorkerThread(self.hWaitDone)
        worker.start()

        l.info("Starting run function")
        while True:
            rc = win32event.WaitForMultipleObjects([self.hWaitStop, self.hWaitDone],False, win32event.INFINITE)
            l.info("wait for multiple objects")
            if rc == 0:
                        # Stop signal encountered
                        servicemanager.LogInfoMsg(self._svc_name_ + " - STOPPED!")  #For Event Log
                        break

            if rc == 1:
                        # Wait until worker has fully finished
                        get_current_process_info()
                        worker.join()
                        # # Determine from worker state if we need to start again (because run finished)
                        # # Or do whatever
                        # if not worker.need_to_start_again():
                        #     break
                        worker = WorkerThread(self.hWaitDone)
                        worker.start()
                        print_ids(worker)
                        





    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        i = 0
        #while True:
            # '''
            # random.seed()
            # x = random.randint(1, 1000000)
            # Path(f'c:{x}.txt').touch()
            # '''
        time.sleep(5)

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()