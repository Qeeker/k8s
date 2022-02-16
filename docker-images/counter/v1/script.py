import time
import signal
import sys


def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

print("Counter v1")
i = 0
while True:
    i += 1
    print(i)
    sys.stdout.flush()
    time.sleep(2)
