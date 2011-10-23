#!/bin/bash
virtualenv --no-site-packages env
source env/bin/activate
pip install -r requirements.txt