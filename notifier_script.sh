#!/bin/bash
set -euo pipefail

cd $(find ~ -name "covid-vaccine-notifier-browser" 2> /dev/null)
source venv_browser/bin/activate
while true
do
  python3 browser_notifier.py
  echo "Last ran on: $(date +%d-%m-%Y) at $(date +%T)" >> logs$(date +_%d_%m_%Y).txt
  sleep 30
done
