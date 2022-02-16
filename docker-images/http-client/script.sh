#!/bin/bash

set -e

trap "exit 0" SIGQUIT
trap "exit 0" SIGTERM
trap "exit 0" SIGINT

while true; do
   curl -s http://${TARGET:-localhost}/ || true
   sleep 2
done