import threading
import os
from pylsl import resolve_stream

def quit_function(fn_name):
    print('{0} took too long, terminating...'.format(fn_name))
    os._exit(00)

def exit_after(s):
    #used as decorator to exit process if function takes longer than s seconds
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

@exit_after(10)
def resolve_conn():
    print("Looking for an EEG stream...")
    print("Process will terminate after 10 seconds if no device found")
    return resolve_stream('type', 'EEG')