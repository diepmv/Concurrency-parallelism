from collections import deque
from threading import Thread, Lock
import time


class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()
    def put(self, item):
        with self.lock:
            self.items.append(item)
    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01) # No work to do
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()

threads = [
	Worker(download, download_queue, resize_queue),
	Worker(resize, resize_queue, upload_queue),
	Worker(upload, upload_queue, done_queue)
]


for thread in threads:
  thread.start()

for _ in range(1000):
  download_queue.put(object())

while len(done_queue.items) < 1000:
  # Do something useful while waiting
  pass

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)

print("Processed", processed, 'items after polling', polled, 'times')


##########################
#Queue
##########################

from Queue import Queue
from threading import Thread

queue = Queue(1)

def consumer():
    time.sleep(0.1)
    print("consumer waiting")
    queue.get()
    print("consumer done")

thread = Thread(target=consumer)
thread.start()
print("producer putting")
queue.put(object())
thread.join()

print("producer done")


class ClosableQueue(Queue):
  SETINEL = object()

  def close(self):
    self.put(self.SENTINEL)

  def __iter__(self):
    while True:
      item = self.get()
      try:
        if item is self.SENTINEL:
          return # Cause the thread to exit
        yield item
      finally:
        self.task_done()

class StoppableWorker(Thread):
  def __init__(self, func, in_queue, out_queue):
     pass

  def run(self):
    for item in self.in_queue:
      result = self.func(item)
      self.out_queue.put(result)

download_queue = ClosableQueue()
# 
threads = [StoppableWorker(download, download_queue, resize_queue),
#
]

for thread in threads:
  thread.start()

for _ in range(1000):
  download_queue.put(object())

download_queue.close()

download_queue.join()
resize_queue.close()

resize_queue.join()
upload_queue.close()
upload_queue.join()

print(done_queue.qsize(), 'items finished')

