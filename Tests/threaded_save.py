from PIL import Image

import sys, time
import cStringIO
import threading, Queue

try:
    format = sys.argv[1]
except:
    format = "PNG"

im = Image.open("Images/lena.ppm")
im.load()

queue = Queue.Queue()

result = []

class Worker(threading.Thread):
    def run(self):
        while 1:
            im = queue.get()
            if im is None:
                queue.task_done()
                sys.stdout.write("x")
                break
            f = cStringIO.StringIO()
            im.save(f, format, optimize=1)
            data = f.getvalue()
            result.append(len(data))
            im = Image.open(cStringIO.StringIO(data))
            im.load()
            sys.stdout.write(".")
            queue.task_done()

t0 = time.time()

threads = 20
jobs = 100

for i in range(threads):
    w = Worker()
    w.start()

for i in range(jobs):
    queue.put(im)

for i in range(threads):
    queue.put(None)

queue.join()

print
print time.time() - t0
print len(result), sum(result)
print result
