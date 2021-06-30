from threading import Thread
from typing import Any

from pymitter import EventEmitter


class AsyncEventEmitter:
    def __init__(self):
        self._emitter = EventEmitter()

    def emit(self, *args, **kwargs):
        return self._emitter.emit(*args, **kwargs)

    def on(self, event: Any, func: Any, ttl: int = -1, asynchronous: bool = True):
        # Determine if we want to handle this synchronously or asynchronously
        if asynchronous:
            # Create a function which wraps our function in a new thread
            def wrapped_func(*args, **kwargs):
                thread = Thread(target=func, args=args, kwargs=kwargs)
                thread.start()

            return self._emitter.on(event=event, func=wrapped_func, ttl=ttl)
        else:
            return self._emitter.on(event=event, func=func, ttl=ttl)
