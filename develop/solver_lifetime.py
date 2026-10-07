"""Defer SIGINT exceptions until timer cleanup and solver disposal complete."""
from contextlib import contextmanager
import signal


@contextmanager
def deferred_interrupt():
    state = {'pending': False, 'callback': None}
    previous = signal.getsignal(signal.SIGINT)

    def remember_interrupt(signum, frame):
        state['pending'] = True
        if state['callback'] is not None:
            state['callback']()

    if previous == signal.SIG_IGN:
        yield state
        return
    signal.signal(signal.SIGINT, remember_interrupt)
    try:
        yield state
    finally:
        signal.signal(signal.SIGINT, previous)
        if state['pending']:
            if callable(previous):
                previous(signal.SIGINT, None)
            else:
                raise KeyboardInterrupt
