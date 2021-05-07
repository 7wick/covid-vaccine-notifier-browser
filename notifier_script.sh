#!/bin/bash

cd $(find ~ -name "browser_vaccine_notifier" 2> /dev/null)
source venv_browser/bin/activate
while true
do
  python3 browser_notifier.py
  echo "Last ran on: $(date +%d-%m-%Y) at $(date +%T)" >> logs.txt
  sleep 30
done
