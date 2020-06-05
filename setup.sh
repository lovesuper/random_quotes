#!/usr/bin/env bash
rm -rf .env
virtualenv -p python3 .env
. .env/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:user@localhost/quotes_db
