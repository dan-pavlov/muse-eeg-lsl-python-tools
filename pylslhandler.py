import threading
import os

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