import signal
import sys
import time


def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

print("Counter v2")
print("="*80)
i = 0
while True:
    i += 1
    print(f"Iteration: {i}")
    print("=" * 80)
    sys.stdout.flush()
    time.sleep(2)
