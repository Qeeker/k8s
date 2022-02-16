import time
import signal
import sys
from pathlib import Path
import socket


def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

i = 0
while True:
    i += 1
    Path("/data/index.html").write_text(f"<h1>Hello World {i} [{socket.gethostname()}]</h1>\n")
    time.sleep(2)
