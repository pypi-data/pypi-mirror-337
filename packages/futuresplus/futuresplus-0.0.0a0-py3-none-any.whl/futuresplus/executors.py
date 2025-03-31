import os
import time
from concurrent import futures

from threading import Thread, current_thread
from typing import List

from concurrent.futures import ThreadPoolExecutor

def print_number(num: int):
    time.sleep(5)
    print(f"Thread: {current_thread().name} {num}")

class ThreadPool:
    max_workers: int
    _thread_name_prefix: str
    _threads: List[Thread]

    def __init__(self, max_workers: int = os.cpu_count(), thread_name_prefix: str = "Thread_"):
        self.max_workers = max_workers
        self._thread_name_prefix = thread_name_prefix
        self._threads = list()

    def __enter__(self):
        for thread_id in range(self.max_workers):
            t = Thread(target=print_number, args=(thread_id, ), name=f"{self._thread_name_prefix}{thread_id}")
            self._threads.append(t)
            t.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for thread in self._threads:
            thread.join()

with ThreadPool(max_workers=10) as tp:
    ...

class PriorityThreadPoolExecutor(futures._base.Executor):
    ...