"""
You can also pipe data from your Python program into a subprocess and retrieve its
output. This allows you to utilize other programs to do work in parallel. For example, say
you want to use the openssl command-line tool to encrypt some data. Starting the child
process with command-line arguments and I/O pipes is easy.
"""

import os
import subprocess


def run_openssl(data):
  env = os.environ.copy()
  env["password"] = b'\xe24U\n\xd0Ql3S\x11'
  proc = subprocess.Popen(["openssl", "enc", "-des3", "-pass", "env:password"], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

  proc.stdin.write(data)
  proc.stdin.flush() # ensure the child gets input

  return proc

"""
Here, I pipe random bytes into the encryption function, but in practice this would be user
input, a file handle, a network socket, etc.:
"""

procs = []

for _ in range(3):
  data = os.urandom(10)
  proc = run_openssl(data)
  procs.append(proc)


"""
The child processes will run in parallel and consume their input. Here, I wait for them to
finish and then retrieve their final output:
"""

for proc in procs:
  out, error = proc.communicate()
  print(out[-10:])




