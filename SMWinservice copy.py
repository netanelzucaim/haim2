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

import socket
import time
import win32serviceutil

import servicemanager
import win32event
import win32service

import threading

class InterruptedException(Exception):
    pass

class WorkerThread(threading.Thread):
    def __init__(self, controller):
        self._controller = controller
    #    self._stop = threading.Event()
        super(WorkerThread, self).__init__()

    # def stop(self):
    #     self._stop.set()

    # def stopped(self):
    #     return self._stop.isSet()

    def run(self):
        try:
           # Insert the code you want to run as a service here
           # rather than do "execfile(.../.../blah)" simply do:
           # You can have your code throw InterruptedException if your code needs to exit
           # Also check often if self.stopped and then cleanly exit
            '''
            Called when the service is asked to start
            '''
            l.info("run function")
            time.sleep(10)
           # if code in another module is not yours or cannot check often if it should stop then use multiprocessing which will spawn separate processes that you can terminate then from here when you need to stop and return
           # in that case simply block here on self._stop.wait()
            l.info("finish sleeping 10")

        except InterruptedException as exc:
           # We are forcefully quitting 
           pass
        except Exception as e:
           # Oh oh, did not anticipate this, better report to Windows or log it
            l.error("exception")
        finally:
           # Close/release any connections, handles, files etc.

           # OK, we can stop now
           l.info("before setevent ")

           win32event.SetEvent(self._controller)
           l.info("after setevent")

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

    # def __init__(self, args):
    #     '''
    #     Constructor of the winservice
    #     '''
    #     l.info("constructor")
    #     win32serviceutil.ServiceFramework.__init__(self, args)
    #     self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    #     socket.setdefaulttimeout(60)
    #     l.info("finish constructor")
        
    def __init__(self, args):
        l.info("constructor")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)      
        self.hWaitDone = win32event.CreateEvent(None, 0, 0, None)
        l.info("finish constructor")




    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        l.info("Stop request received")
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

# '''
#     def SvcDoRun(self):
#         self.start()
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STARTED,
#                               (self._svc_name_, ''))
#         l.info("Starting service")

#         self.main()
# '''
    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        l.info("calling start service")

        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 

        worker = WorkerThread(self.hWaitDone)

        worker.start()
        l.info("before join")

        worker.join()
        l.info("sleep finished")
        while True:
            # Wait for service stop signal
            l.info("before rc")
            rc = win32event.WaitForMultipleObjects([self.hWaitStop, self.hWaitDone], win32event.INFINITE)
            rc = 1
            l.info("after rc")

            # Check to see if self.hWaitStop happened as part of Windows Service Management
            if rc == 0:
                # Stop signal encountered
                servicemanager.LogInfoMsg(self._svc_name_ + " - STOPPED!")  #For Event Log
                break

            if rc == 1:
                # Wait until worker has fully finished
                worker.join()

                # Determine from worker state if we need to start again (because run finished)
                # Or do whatever
                if not worker.need_to_start_again():
                    break

                worker.start()




    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    # def stop(self):
    #     '''
    #     Override to add logic before the stop
    #     eg. invalidating running condition
    #     '''
    #     pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()