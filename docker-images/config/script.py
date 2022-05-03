import signal
import sys
import time
import os
from datetime import datetime
from pathlib import Path

def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)


while True:
    print(datetime.now().strftime(" %d.%m.%Y %H:%M:%S ").center(80, "="))
    print(" Environment ".center(80, "="))
    print(f"FILE_COMMON={os.environ['FILE_COMMON']}")
    print(f"DEPLOYMENT_ENV={os.environ['DEPLOYMENT_ENV']}")
    print(" Config file ".center(80, "="))
    print(Path("/config/cfg").read_text().strip())
    print("".center(80, "="))
    print()
    sys.stdout.flush()
    time.sleep(2)
