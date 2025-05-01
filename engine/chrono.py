
import time

_last_times = {}

def every(x, key="default"): #cada x min
    now = time.time()
    last = _last_times.get(key, 0)
    if now - last >= x:
        _last_times[key] = now
        return True
    return False
