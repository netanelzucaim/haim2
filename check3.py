
from time import sleep, perf_counter
from threading import Thread
import threading

class InterruptedException(Exception):
    pass

class WorkerThread(threading.Thread):


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

           sleep(5)
           worker.stop
           # if code in another module is not yours or cannot check often if it should stop then use multiprocessing which will spawn separate processes that you can terminate then from here when you need to stop and return
           # in that case simply block here on self._stop.wait()

        except InterruptedException as exc:
           # We are forcefully quitting 
           pass
        except Exception as e:
           # Oh oh, did not anticipate this, better report to Windows or log it
           print('exception')
        finally:
           # Close/release any connections, handles, files etc.

           # OK, we can stop now
           print("hi")

if __name__ == '__main__':

    worker = WorkerThread()
    worker.start()
    i=1
    while i<5:
            # Wait until worker has fully finished
            worker.join()

            # Determine from worker state if we need to start again (because run finished)
            # Or do whatever

            i=i+1
            worker.start()




