import hashlib
import os
import signal
import sys
import time


def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

print("Config reader")
print("="*80)

processed_fingerprint = None

while True:
    try:
        # Read config
        with open(os.environ.get("CFG_FILE", "/default/default.cfg"), "rb") as fp:
            cfg = fp.read()

        # Get fingerprint
        current_fingerprint = hashlib.sha1(cfg).hexdigest()
        if current_fingerprint != processed_fingerprint:
            processed_fingerprint = current_fingerprint
            print("Loaded config")
            print("="*80)
            print(cfg.decode())
            print("="*80)
    except Exception as e:
        print(f"Loading config failed. Reason: {e}")
    sys.stdout.flush()
    time.sleep(2)
