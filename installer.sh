#!/bin/bash
set -euo pipefail

cd $(find ~ -name "covid-vaccine-notifier-browser" 2> /dev/null)
echo "Installing virtualenv"
pip install virtualenv
echo "Creating your virtual environment"
virtualenv venv_browser
echo "Activating your virtual environment"
source venv_browser/bin/activate
echo "Installing python modules"
pip install -r requirements.txt
echo "Setup done!"
