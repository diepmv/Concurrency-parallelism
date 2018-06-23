"""
Child processes will run independently from their parent process, the Python interpreter.
Their status can be polled periodically while Python does other work.
"""

proc = subprocess.Popen([‘sleep’, ‘3’])
while proc.poll() is None:
  print(‘Working...’)
  # Some time-consuming work here
  # ...

print(‘Exit status’, proc.poll())
