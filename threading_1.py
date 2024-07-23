
import threading

class InterruptedException(Exception):
    pass

class WorkerThread(threading.Thread):
    def __init__(self, controller):
        self._controller = controller
        self._stop = threading.Event()
        super(WorkerThread, self).__init__()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        try:
           # Insert the code you want to run as a service here
           # rather than do "execfile(.../.../blah)" simply do:
           # You can have your code throw InterruptedException if your code needs to exit
           # Also check often if self.stopped and then cleanly exit

           import your_file
           your_file.main()

           # if code in another module is not yours or cannot check often if it should stop then use multiprocessing which will spawn separate processes that you can terminate then from here when you need to stop and return
           # in that case simply block here on self._stop.wait()

        except InterruptedException as exc:
           # We are forcefully quitting 
           pass
        except Exception as e:
           # Oh oh, did not anticipate this, better report to Windows or log it
        finally:
           # Close/release any connections, handles, files etc.

           # OK, we can stop now
           win32event.SetEvent(self._controller)