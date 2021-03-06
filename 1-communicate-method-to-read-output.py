"""
Running a child process with subprocess is simple. Here, the Popen constructor starts
the process. The communicate method reads the child process’s output and waits for
termination
"""

import subprocess

proc = subprocess.Popen(['echo', "Hello from child!"],
			 stdout=subprocess.PIPE)

out, error = proc.communicate()

print(out.decode('utf-8'))
