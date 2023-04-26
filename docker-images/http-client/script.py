import os
import signal
import sys
import time
import urllib.request
from http.client import HTTPResponse

def sig_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

while True:
    response: HTTPResponse = urllib.request.urlopen(f"http://{os.environ['TARGET']}/")
    print(response.read().decode("utf-8"))
    sys.stdout.flush()
    time.sleep(2)
