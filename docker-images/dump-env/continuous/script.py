import os
import signal
import sys
import time


def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

print("Continuous Environment Dumper")
print("=" * 80)

while True:
    for k, v in os.environ.items():
        print(f"{k}={v}")
    print("=" * 80)
    sys.stdout.flush()
    time.sleep(2)
