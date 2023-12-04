import threading

class MCFThread(threading.Thread):
    def __init__(self, func, region, args=False):
        super().__init__()
        self._target = func
        self.daemon = True
        self.name = f"{func.__name__}-Thr_{region}"
        if args:
            self._args = args