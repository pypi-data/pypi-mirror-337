"""File that stores useful commands and a small test code for profiling."""
import numpy as np

# check for line_profiler or memory_profiler in the local scope, both
# are injected by their respective tools or they're absent
# if these tools aren't being used (in which case we need to substitute
# a dummy @profile decorator)
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner

@profile
def main():
    a = np.ones((100000, 2))
    b = np.empty(100000)

    np.copyto(b, a[:, 1])
    b[:] = a[:, 1]

if __name__ == "__main__":
    main()
    
# kernprof -l -v ./profiling.py
# python -m memory_profiler ./profiling.py  