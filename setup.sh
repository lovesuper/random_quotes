#!/usr/bin/env bash
rm -rf .env
virtualenv -p python3 .env --no-site-packages
. .env/bin/activate
pip install -r requirements.txt
