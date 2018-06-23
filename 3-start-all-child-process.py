"""
Decoupling the child process from the parent means that the parent process is free to run
many child processes in parallel. You can do this by starting all the child processes
together upfront.


"""
import time
import process

def run_sleep(period):
  proc = subprocess.Popen(['sleep', str(period)])
  return proc

start = time()
procs = []

for _ in range(10):
  proc = run_sleep(0.1)
  procs.append(proc)

# Later, you can wait for them to finish their I/O and terminate with the communicate method.

for proc in procs:
  proc.communicate()

end = time()

print("Finished in %.3f seconds" % (end-start))
 # If these processes ran in sequence, the total delay would be 1 second, not the ~0.1 second I measured.
